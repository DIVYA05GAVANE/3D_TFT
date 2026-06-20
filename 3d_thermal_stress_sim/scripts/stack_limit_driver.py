#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import meshio
import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = ROOT / "inputs"
THREEDICE = Path(os.environ.get("THREEDICE", shutil.which("3D-ICE-Emulator") or "3D-ICE-Emulator"))
ELMER_IMAGE = os.environ.get("ELMER_IMAGE", "eperera/elmerfem")
GMSH = os.environ.get("GMSH", "gmsh")

CHIP_L_UM = 20000.0
CHIP_W_UM = 20000.0
INITIAL_TEMP_C = 27.0
TEMP_LIMIT_C = 85.0
WARPAGE_LIMIT_UM = 50.0
THERMAL_CELL_UM = 4000.0
SUBSTRATE_UM = 500.0

MATERIALS_3DICE = """
material SILICON :
   thermal conductivity     1.30e-4 ;
   volumetric heat capacity 1.628e-12 ;

material SIO2 :
   thermal conductivity     1.40e-6 ;
   volumetric heat capacity 1.55e-12 ;

material AL2O3 :
   thermal conductivity     3.00e-5 ;
   volumetric heat capacity 3.03e-12 ;

material HFO2 :
   thermal conductivity     5.00e-7 ;
   volumetric heat capacity 2.50e-12 ;

material HZO :
   thermal conductivity     1.00e-6 ;
   volumetric heat capacity 2.60e-12 ;

material ZNO :
   thermal conductivity     5.00e-5 ;
   volumetric heat capacity 2.80e-12 ;

material TUNGSTEN :
   thermal conductivity     1.74e-4 ;
   volumetric heat capacity 2.58e-12 ;

material NICKEL :
   thermal conductivity     9.00e-5 ;
   volumetric heat capacity 3.95e-12 ;

material BEOL :
   thermal conductivity     2.25e-6 ;
   volumetric heat capacity 2.175e-12 ;
""".strip()


@dataclass
class MechMaterial:
    name: str
    E_GPa: float
    nu: float
    alpha_ppm_K: float
    residual_MPa: float
    allowable_MPa: float

    @property
    def biaxial_MPa(self) -> float:
        return self.E_GPa * 1000.0 / (1.0 - self.nu)


MAT: Dict[str, MechMaterial] = {
    # The residual stresses and allowables are screening assumptions, not measured PDK values.
    "W": MechMaterial("W", 400.0, 0.28, 4.5, 300.0, 750.0),
    "Ni": MechMaterial("Ni", 200.0, 0.31, 13.4, 120.0, 250.0),
    "SiO2": MechMaterial("SiO2", 70.0, 0.17, 0.5, -100.0, 500.0),
    "Al2O3": MechMaterial("Al2O3", 300.0, 0.22, 7.5, -150.0, 700.0),
    "HfO2": MechMaterial("HfO2", 180.0, 0.30, 5.5, -200.0, 600.0),
    "HZO": MechMaterial("HZO", 170.0, 0.30, 6.0, -250.0, 600.0),
    "ZnO": MechMaterial("ZnO", 140.0, 0.34, 4.0, 150.0, 250.0),
    "BondSiO2": MechMaterial("BondSiO2", 70.0, 0.17, 0.5, -50.0, 350.0),
    "Si": MechMaterial("Si", 130.0, 0.28, 2.6, 0.0, 7000.0),
}

@dataclass
class Layer:
    name: str
    mat_key: str
    thickness_um: float
    tier: str
    pair_index: int

    @property
    def material(self) -> MechMaterial:
        return MAT[self.mat_key]


def run(cmd: List[str], cwd: Optional[Path] = None, timeout: int = 300, log: Optional[Path] = None) -> subprocess.CompletedProcess:
    proc = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
    if log:
        log.write_text(proc.stdout)
    return proc


def load_floorplans() -> Tuple[Path, Path]:
    fefet = INPUT_DIR / "fefet_tier.flp"
    tft = INPUT_DIR / "tft_tier.flp"
    if not fefet.exists() or not tft.exists():
        raise FileNotFoundError("expected inputs/fefet_tier.flp and inputs/tft_tier.flp")
    return fefet, tft


def write_3dice_stack(case_dir: Path, n_pairs: int, order: str, thermal_cell_um: float) -> Path:
    fefet_src, tft_src = load_floorplans()
    shutil.copy2(fefet_src, case_dir / "fefet_tier.flp")
    shutil.copy2(tft_src, case_dir / "tft_tier.flp")
    stack = case_dir / f"stack_{order}_{n_pairs:04d}.stk"
    temp_k = INITIAL_TEMP_C + 273.15
    with stack.open("w") as f:
        f.write(MATERIALS_3DICE + "\n\n")
        f.write("top heat sink :\n")
        f.write("   heat transfer coefficient 1.0e-7 ;\n")
        f.write(f"   temperature               {temp_k:.6f} ;\n\n")
        f.write("dimensions :\n")
        f.write(f"   chip length {CHIP_L_UM:.6f}, width {CHIP_W_UM:.6f} ;\n")
        f.write(f"   cell length {thermal_cell_um:.6f}, width {thermal_cell_um:.6f} ;\n")
        f.write("   non-uniform false ;\n\n")
        f.write("layer BOND_LAYER :\n   height 0.100 ;\n   material SIO2 ;\n\n")
        f.write(f"layer SI_SUBSTRATE :\n   height {SUBSTRATE_UM:.6f} ;\n   material SILICON ;\n\n")
        f.write("die FEFET_DIE :\n")
        f.write("   layer 0.040 TUNGSTEN ;\n   source 0.016 HZO ;\n   layer 0.040 AL2O3 ;\n   layer 0.100 SIO2 ;\n\n")
        f.write("die TFT_DIE :\n")
        f.write("   layer 0.060 NICKEL ;\n   layer 0.040 AL2O3 ;\n   source 0.007 ZNO ;\n   layer 0.015 HFO2 ;\n   layer 0.100 SIO2 ;\n\n")
        f.write("stack:\n")
        entries: List[Tuple[str, str, str]] = []
        for i in range(n_pairs, 0, -1):
            if order == "fefet_on_tft":
                entries += [(f"FEFET_{i:04d}", "FEFET_DIE", "fefet_tier.flp"), (f"TFT_{i:04d}", "TFT_DIE", "tft_tier.flp")]
            else:
                entries += [(f"TFT_{i:04d}", "TFT_DIE", "tft_tier.flp"), (f"FEFET_{i:04d}", "FEFET_DIE", "fefet_tier.flp")]
        for idx, (die_id, die_type, flp) in enumerate(entries):
            f.write(f"   die     {die_id:<12} {die_type:<10} floorplan \"{flp}\" ;\n")
            if idx != len(entries) - 1:
                f.write(f"   layer   BOND_{idx:04d}    BOND_LAYER ;\n")
        f.write("   layer   HANDLE_SUBSTRATE SI_SUBSTRATE ;\n")
        f.write("   layer   PCB_ATTACH BOND_LAYER ;\n\n")
        f.write("solver:\n   steady ;\n")
        f.write(f"   initial temperature {temp_k:.6f} ;\n   numofcores 1 ;\n\n")
        f.write("output:\n")
        for die_id, _, _ in entries:
            f.write(f"   Tflp( {die_id}, \"max_{die_id}.txt\", maximum, final ) ;\n")
            f.write(f"   Tflp( {die_id}, \"avg_{die_id}.txt\", average, final ) ;\n")
        # Keep one full map per case, enough for ParaView/plot inspection without huge output.
        f.write(f"   Tmap( {entries[0][0]}, \"tmap_top.txt\", final ) ;\n")
        f.write(f"   Tmap( {entries[-1][0]}, \"tmap_bottom.txt\", final ) ;\n")
    return stack


def parse_scalar_output(path: Path) -> Optional[float]:
    if not path.exists():
        return None
    value = None
    for line in path.read_text(errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("%"):
            continue
        parts = line.split()
        try:
            value = float(parts[-1])
        except Exception:
            pass
    return value


def run_thermal_case(n_pairs: int, order: str, thermal_cell_um: float) -> Dict[str, object]:
    case_dir = ROOT / "thermal_runs" / order / f"pairs_{n_pairs:04d}"
    if case_dir.exists():
        shutil.rmtree(case_dir)
    case_dir.mkdir(parents=True)
    stack = write_3dice_stack(case_dir, n_pairs, order, thermal_cell_um)
    proc = run([str(THREEDICE), stack.name], cwd=case_dir, timeout=600, log=case_dir / "3dice.log")
    max_vals = []
    avg_vals = []
    for f in case_dir.glob("max_*.txt"):
        v = parse_scalar_output(f)
        if v is not None:
            max_vals.append(v - 273.15)
    for f in case_dir.glob("avg_*.txt"):
        v = parse_scalar_output(f)
        if v is not None:
            avg_vals.append(v - 273.15)
    return {
        "order": order,
        "pairs": n_pairs,
        "tiers": 2 * n_pairs,
        "rc": proc.returncode,
        "thermal_case_dir": str(case_dir),
        "peak_temp_C": max(max_vals) if max_vals else float("nan"),
        "avg_die_temp_C": sum(avg_vals) / len(avg_vals) if avg_vals else float("nan"),
        "log_tail": "\n".join((case_dir / "3dice.log").read_text(errors="replace").splitlines()[-10:]),
    }


def pair_layers(order: str, pair_index: int) -> List[Layer]:
    # bottom-to-top order for one pair. If the process says FeFET-on-TFT, TFT is below FeFET.
    tft = [
        Layer("TFT_SiO2", "SiO2", 0.100, "TFT", pair_index),
        Layer("TFT_HfO2", "HfO2", 0.015, "TFT", pair_index),
        Layer("TFT_ZnO", "ZnO", 0.007, "TFT", pair_index),
        Layer("TFT_Al2O3", "Al2O3", 0.040, "TFT", pair_index),
        Layer("TFT_Ni", "Ni", 0.060, "TFT", pair_index),
    ]
    fefet = [
        Layer("FEFET_SiO2", "SiO2", 0.100, "FEFET", pair_index),
        Layer("FEFET_Al2O3", "Al2O3", 0.040, "FEFET", pair_index),
        Layer("FEFET_HZO", "HZO", 0.016, "FEFET", pair_index),
        Layer("FEFET_W", "W", 0.040, "FEFET", pair_index),
    ]
    bond = [Layer("Bond_SiO2", "BondSiO2", 0.100, "BOND", pair_index)]
    if order == "fefet_on_tft":
        return tft + bond + fefet
    return fefet + bond + tft


def build_layers(n_pairs: int, order: str) -> List[Layer]:
    layers: List[Layer] = [Layer("Si_handle_substrate", "Si", SUBSTRATE_UM, "SUBSTRATE", 0)]
    for i in range(1, n_pairs + 1):
        if i > 1:
            layers.append(Layer("InterPair_Bond_SiO2", "BondSiO2", 0.100, "BOND", i))
        layers.extend(pair_layers(order, i))
    return layers


def laminate_solve(layers: List[Layer], temp_c: float) -> Dict[str, object]:
    z_edges = [0.0]
    for layer in layers:
        z_edges.append(z_edges[-1] + layer.thickness_um * 1e-6)
    total_t = z_edges[-1]
    z_mid = total_t / 2.0
    zs = [z - z_mid for z in z_edges]
    dT = temp_c - INITIAL_TEMP_C
    A = B = D = 0.0
    NT = MT = 0.0
    layer_rows = []
    for layer, z0, z1 in zip(layers, zs[:-1], zs[1:]):
        mat = layer.material
        M = mat.biaxial_MPa
        alpha = mat.alpha_ppm_K * 1e-6
        residual_eigen = mat.residual_MPa / M
        eigen = alpha * dT + residual_eigen
        dz = z1 - z0
        dz2 = 0.5 * (z1 * z1 - z0 * z0)
        dz3 = (z1**3 - z0**3) / 3.0
        A += M * dz
        B += M * dz2
        D += M * dz3
        NT += M * eigen * dz
        MT += M * eigen * dz2
    mat2 = np.array([[A, B], [B, D]], dtype=float)
    rhs = np.array([NT, MT], dtype=float)
    eps0, kappa = np.linalg.solve(mat2, rhs)
    max_ratio = 0.0
    max_vm = 0.0
    worst = None
    for idx, (layer, z0, z1) in enumerate(zip(layers, zs[:-1], zs[1:]), start=1):
        mat = layer.material
        M = mat.biaxial_MPa
        alpha = mat.alpha_ppm_K * 1e-6
        residual_eigen = mat.residual_MPa / M
        eigen = alpha * dT + residual_eigen
        zc = 0.5 * (z0 + z1)
        stress = M * (eps0 + kappa * zc - eigen)
        vm = abs(stress)
        ratio = vm / mat.allowable_MPa
        row = {
            "idx": idx,
            "name": layer.name,
            "material": mat.name,
            "tier": layer.tier,
            "pair_index": layer.pair_index,
            "z0_um": (z0 + z_mid) * 1e6,
            "z1_um": (z1 + z_mid) * 1e6,
            "stress_MPa": stress,
            "von_mises_MPa": vm,
            "allowable_MPa": mat.allowable_MPa,
            "failure_ratio": ratio,
        }
        layer_rows.append(row)
        if ratio > max_ratio:
            max_ratio = ratio
            max_vm = vm
            worst = row
    L_m = CHIP_L_UM * 1e-6
    warpage_um = abs(kappa) * L_m * L_m / 8.0 * 1e6
    return {
        "total_thickness_um": total_t * 1e6,
        "eps0": eps0,
        "curvature_1_per_m": kappa,
        "warpage_um": warpage_um,
        "max_von_mises_MPa": max_vm,
        "max_failure_ratio": max_ratio,
        "worst_layer": worst,
        "layer_rows": layer_rows,
    }


def write_gmsh_geo(layers: List[Layer], path: Path, mesh_lc_um: float = 2000.0) -> None:
    # 2D cross-section in micrometers, x along chip length and z through stack thickness.
    lines = ["SetFactory(\"OpenCASCADE\");", f"lc = {mesh_lc_um};"]
    z = 0.0
    rect_ids = []
    for i, layer in enumerate(layers, start=1):
        h = max(layer.thickness_um, 0.001)
        lines.append(f"Rectangle({i}) = {{0, {z:.9f}, 0, {CHIP_L_UM:.9f}, {h:.9f}, 0}};")
        lines.append(f"Physical Surface(\"{layer.mat_key}_{i:04d}\", {1000+i}) = {{{i}}};")
        rect_ids.append(i)
        z += h
    lines.append("Coherence;")
    lines.append("Mesh.Algorithm = 6;")
    lines.append("Mesh.CharacteristicLengthMin = lc;")
    lines.append("Mesh.CharacteristicLengthMax = lc;")
    path.write_text("\n".join(lines) + "\n")


def write_vtu_from_laminate(layers: List[Layer], mech: Dict[str, object], path: Path, temp_c: float) -> None:
    # Create a simple structured cross-section mesh directly, with cell data per layer.
    nx = 80
    points = []
    cells = []
    stress = []
    ratio = []
    material_id = []
    temp = []
    layer_rows = mech["layer_rows"]
    kappa = float(mech["curvature_1_per_m"])
    L = CHIP_L_UM
    for li, row in enumerate(layer_rows):
        z0 = float(row["z0_um"])
        z1 = float(row["z1_um"])
        base_idx = len(points)
        for ix in range(nx + 1):
            x = CHIP_L_UM * ix / nx
            w_um = 0.5 * kappa * ((x - L / 2.0) * 1e-6) ** 2 * 1e6
            points.append([x, 0.0, z0 + w_um])
        for ix in range(nx + 1):
            x = CHIP_L_UM * ix / nx
            w_um = 0.5 * kappa * ((x - L / 2.0) * 1e-6) ** 2 * 1e6
            points.append([x, 0.0, z1 + w_um])
        for ix in range(nx):
            cells.append([base_idx + ix, base_idx + ix + 1, base_idx + (nx + 1) + ix + 1, base_idx + (nx + 1) + ix])
            stress.append(float(row["von_mises_MPa"]))
            ratio.append(float(row["failure_ratio"]))
            material_id.append(li + 1)
            temp.append(temp_c)
    mesh = meshio.Mesh(
        points=np.array(points, dtype=float),
        cells=[("quad", np.array(cells, dtype=int))],
        cell_data={
            "von_mises_MPa": [np.array(stress)],
            "failure_ratio": [np.array(ratio)],
            "material_id": [np.array(material_id)],
            "temperature_C": [np.array(temp)],
        },
    )
    mesh.write(path)


def write_elmer_sif(layers: List[Layer], path: Path, temp_c: float, title: str) -> None:
    # Elmer-ready deck for the Gmsh cross-section. Generated as a starting point for full FEM.
    mats_seen: Dict[str, int] = {}
    for layer in layers:
        if layer.mat_key not in mats_seen:
            mats_seen[layer.mat_key] = len(mats_seen) + 1
    lines = [
        "Header",
        "  CHECK KEYWORDS Warn",
        "  Mesh DB \".\" \"mesh\"",
        "  Results Directory \".\"",
        "End",
        "Simulation",
        "  Max Output Level = 5",
        "  Coordinate System = Cartesian 2D",
        "  Simulation Type = Steady state",
        "  Steady State Max Iterations = 1",
        "  Output Intervals = 1",
        "  Solver Input File = case.sif",
        "  Post File = case.ep",
        "End",
        "Equation 1",
        "  Active Solvers(2) = 1 2",
        "End",
        "Solver 1",
        "  Equation = Linear elasticity",
        "  Procedure = \"StressSolve\" \"StressSolver\"",
        "  Variable = -dofs 2 Displacement",
        "  Calculate Stresses = Logical True",
        "  Linear System Solver = Direct",
        "  Linear System Direct Method = UMFPACK",
        "End",
        "Solver 2",
        "  Equation = Result Output",
        "  Procedure = \"ResultOutputSolve\" \"ResultOutputSolver\"",
        "  Output File Name = \"stress_result\"",
        "  Vtu Format = Logical True",
        "End",
    ]
    for key, mid in mats_seen.items():
        mat = MAT[key]
        lines += [
            f"Material {mid}",
            f"  Name = \"{mat.name}\"",
            f"  Youngs Modulus = {mat.E_GPa * 1e9:.6e}",
            f"  Poisson Ratio = {mat.nu:.6f}",
            f"  Heat Expansion Coefficient = {mat.alpha_ppm_K * 1e-6:.6e}",
            f"  Reference Temperature = {INITIAL_TEMP_C + 273.15:.6f}",
            "End",
        ]
    lines += [
        "Body Force 1",
        f"  Temperature = Real {temp_c + 273.15:.6f}",
        "End",
    ]
    # Body ids are generated from physical surfaces in write_gmsh_geo as 1000+i.
    for i, layer in enumerate(layers, start=1):
        lines += [
            f"Body {i}",
            f"  Name = \"{layer.name}_{i}\"",
            f"  Target Bodies(1) = {1000+i}",
            "  Equation = 1",
            f"  Material = {mats_seen[layer.mat_key]}",
            "  Body Force = 1",
            "End",
        ]
    lines += [
        "Boundary Condition 1",
        "  Name = \"pin_left_bottom\"",
        "  Target Boundaries(1) = 1",
        "  Displacement 1 = 0",
        "  Displacement 2 = 0",
        "End",
    ]
    path.write_text("\n".join(lines) + "\n")


def generate_mechanical_artifacts(row: Dict[str, object], order: str) -> Dict[str, object]:
    n = int(row["pairs"])
    temp_c = float(row["peak_temp_C"])
    layers = build_layers(n, order)
    mech = laminate_solve(layers, temp_c)
    out_dir = ROOT / "mechanical" / order / f"pairs_{n:04d}"
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    geo = out_dir / "stack_cross_section.geo"
    msh = out_dir / "stack_cross_section.msh"
    vtu = out_dir / "stress_warpage_reduced_order.vtu"
    sif = out_dir / "case.sif"
    write_gmsh_geo(layers, geo)
    if n <= 256:
        try:
            gmsh_proc = run([GMSH, "-2", str(geo), "-format", "msh2", "-o", str(msh)], timeout=180, log=out_dir / "gmsh.log")
            gmsh_rc = gmsh_proc.returncode
        except subprocess.TimeoutExpired as exc:
            (out_dir / "gmsh.log").write_text(str(exc))
            gmsh_rc = 124
    else:
        (out_dir / "gmsh.log").write_text("Skipped gmsh for high layer count; use VTU reduced-order output or rerun selected case with larger timeout.\n")
        gmsh_rc = -1
    write_vtu_from_laminate(layers, mech, vtu, temp_c)
    write_elmer_sif(layers, sif, temp_c, f"{order}_{n}")
    with (out_dir / "layer_stress.csv").open("w", newline="") as f:
        fields = ["idx", "name", "material", "tier", "pair_index", "z0_um", "z1_um", "stress_MPa", "von_mises_MPa", "allowable_MPa", "failure_ratio"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for lr in mech["layer_rows"]:
            w.writerow({k: lr.get(k, "") for k in fields})
    return {
        "mechanical_dir": str(out_dir),
        "gmsh_rc": gmsh_rc,
        "vtu": str(vtu),
        "geo": str(geo),
        "msh": str(msh),
        "sif": str(sif),
        **{k: v for k, v in mech.items() if k != "layer_rows"},
        "worst_layer_name": mech["worst_layer"]["name"] if mech.get("worst_layer") else "",
        "worst_layer_material": mech["worst_layer"]["material"] if mech.get("worst_layer") else "",
    }


def run_elmer_case(mech_dir: Path) -> Dict[str, object]:
    # Convert mesh using ElmerGrid and attempt ElmerSolver via Docker. SIF is a generated starter deck.
    cmd = [
        "bash", "-lc",
        "ElmerGrid 14 2 stack_cross_section.msh -out mesh > elmergrid.log 2>&1 && ElmerSolver case.sif > elmersolver.log 2>&1",
    ]
    proc = run([
        "sudo", "docker", "run", "--rm", "-v", f"{mech_dir}:/case", "-w", "/case", "--entrypoint", "bash", ELMER_IMAGE, "-lc", cmd[2]
    ], timeout=240, log=mech_dir / "elmer_docker.log")
    return {
        "elmer_rc": proc.returncode,
        "elmer_docker_log": str(mech_dir / "elmer_docker.log"),
        "elmer_solver_log": str(mech_dir / "elmersolver.log"),
        "elmergrid_log": str(mech_dir / "elmergrid.log"),
        "elmer_vtu_exists": bool(list(mech_dir.glob("*.vtu"))),
    }


def decide_failure(row: Dict[str, object]) -> Tuple[bool, List[str]]:
    reasons = []
    if float(row["peak_temp_C"]) >= TEMP_LIMIT_C:
        reasons.append(f"thermal peak {float(row['peak_temp_C']):.2f} C >= {TEMP_LIMIT_C:.1f} C")
    if float(row["max_failure_ratio"]) >= 1.0:
        reasons.append(f"stress ratio {float(row['max_failure_ratio']):.3f} >= 1.0")
    if float(row["warpage_um"]) >= WARPAGE_LIMIT_UM:
        reasons.append(f"warpage {float(row['warpage_um']):.2f} um >= {WARPAGE_LIMIT_UM:.1f} um")
    return bool(reasons), reasons


def plot_summary(rows: List[Dict[str, object]], out: Path) -> None:
    orders = sorted({r["order"] for r in rows})
    fig, axs = plt.subplots(3, 1, figsize=(9, 10), sharex=True)
    for order in orders:
        sub = [r for r in rows if r["order"] == order]
        x = [int(r["pairs"]) for r in sub]
        axs[0].plot(x, [float(r["peak_temp_C"]) for r in sub], marker="o", label=order)
        axs[1].plot(x, [float(r["max_failure_ratio"]) for r in sub], marker="o", label=order)
        axs[2].plot(x, [float(r["warpage_um"]) for r in sub], marker="o", label=order)
    axs[0].axhline(TEMP_LIMIT_C, color="r", linestyle="--", linewidth=1)
    axs[1].axhline(1.0, color="r", linestyle="--", linewidth=1)
    axs[2].axhline(WARPAGE_LIMIT_UM, color="r", linestyle="--", linewidth=1)
    axs[0].set_ylabel("Peak temp (C)")
    axs[1].set_ylabel("Max stress ratio")
    axs[2].set_ylabel("Warpage (um)")
    axs[2].set_xlabel("Repeated FeFET/TFT pairs")
    for ax in axs:
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_xscale("log", base=2)
    fig.tight_layout()
    fig.savefig(out, dpi=180)


def main() -> int:
    global THREEDICE, GMSH
    ap = argparse.ArgumentParser()
    ap.add_argument("--orders", default="fefet_on_tft,tft_on_fefet")
    ap.add_argument("--pairs", default="1,2,4,8,16,32,64")
    ap.add_argument("--thermal-cell-um", type=float, default=THERMAL_CELL_UM)
    ap.add_argument("--three-dice", default=str(THREEDICE), help="Path to 3D-ICE-Emulator, or set THREEDICE")
    ap.add_argument("--gmsh", default=GMSH, help="Path to gmsh, or set GMSH")
    ap.add_argument("--run-elmer", action="store_true")
    args = ap.parse_args()

    THREEDICE = Path(args.three_dice)
    GMSH = args.gmsh
    orders = [x.strip() for x in args.orders.split(",") if x.strip()]
    pair_counts = [int(x) for x in args.pairs.split(",") if x.strip()]
    (ROOT / "generated").mkdir(exist_ok=True)
    (ROOT / "plots").mkdir(exist_ok=True)
    rows: List[Dict[str, object]] = []
    for order in orders:
        for n in pair_counts:
            therm = run_thermal_case(n, order, args.thermal_cell_um)
            mech = generate_mechanical_artifacts(therm, order)
            row = {**therm, **mech}
            fail, reasons = decide_failure(row)
            row["failed"] = fail
            row["failure_reasons"] = "; ".join(reasons)
            rows.append(row)
            print(json.dumps({k: row[k] for k in ["order", "pairs", "peak_temp_C", "max_failure_ratio", "warpage_um", "failed", "failure_reasons"]}, indent=2))
            if args.run_elmer and n in (1, pair_counts[-1]):
                elmer = run_elmer_case(Path(row["mechanical_dir"]))
                row.update(elmer)
    # Determine stacking limit: largest nonfailed count before first failure per order.
    limits = {}
    for order in orders:
        sub = [r for r in rows if r["order"] == order]
        safe = [int(r["pairs"]) for r in sub if not r["failed"]]
        failed = [r for r in sub if r["failed"]]
        limits[order] = {
            "largest_simulated_safe_pairs": max(safe) if safe else 0,
            "first_failed_pairs": int(failed[0]["pairs"]) if failed else None,
            "first_failure_reasons": failed[0]["failure_reasons"] if failed else "none in sweep",
        }
    fields = sorted({k for row in rows for k in row.keys() if k != "worst_layer"})
    with (ROOT / "generated" / "stack_limit_sweep.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fields})
    plot_summary(rows, ROOT / "plots" / "stack_limit_summary.png")
    summary = {
        "workdir": str(ROOT),
        "input_floorplans": {
            "fefet": str(INPUT_DIR / "fefet_tier.flp"),
            "tft": str(INPUT_DIR / "tft_tier.flp"),
        },
        "pair_counts": pair_counts,
        "orders": orders,
        "thermal_cell_um": args.thermal_cell_um,
        "criteria": {
            "temperature_limit_C": TEMP_LIMIT_C,
            "warpage_limit_um": WARPAGE_LIMIT_UM,
            "stress_failure_ratio_limit": 1.0,
        },
        "limits": limits,
        "elmer": {
            "native_ElmerSolver_in_PATH": bool(shutil.which("ElmerSolver")),
            "docker_image": ELMER_IMAGE,
            "run_elmer_requested": args.run_elmer,
        },
        "assumptions": [
            "Thermal power per tier reuses package floorplans copied from the previous ngspice -> 3D-ICE convergence run.",
            "FeFET/array regions remain workload placeholders because no FeFET compact model was found in the current SPICE bundle.",
            "Mechanical stress uses classical laminate theory for the full chip cross-section with assumed residual stresses and allowables; Elmer/Gmsh artifacts are generated for FEM handoff.",
            f"Mechanical and thermal stacks include a {SUBSTRATE_UM:.0f} um silicon handle substrate.",
            "3D-ICE sweep uses a coarse thermal cell for repeated-stack exploration; refine near any candidate limit.",
        ],
    }
    (ROOT / "generated" / "summary.json").write_text(json.dumps(summary, indent=2))
    (ROOT / "FINDINGS.md").write_text(
        "# Stack-Limit Findings\n\n"
        f"Workdir: `{ROOT}`\n\n"
        "## Summary\n\n"
        + json.dumps(summary, indent=2)
        + "\n\n## Main output files\n\n"
        "- `generated/stack_limit_sweep.csv`\n"
        "- `generated/summary.json`\n"
        "- `plots/stack_limit_summary.png`\n"
        "- `mechanical/<order>/pairs_*/stress_warpage_reduced_order.vtu`\n"
        "- `mechanical/<order>/pairs_*/case.sif`\n"
        "- `mechanical/<order>/pairs_*/stack_cross_section.geo` and `.msh`\n"
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
