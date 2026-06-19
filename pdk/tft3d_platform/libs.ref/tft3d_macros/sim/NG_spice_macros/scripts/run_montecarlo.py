#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
import re
import shutil
import subprocess
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

DECK_TIMEOUT_S = 240
SEED_DEFAULT = 20260620
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "montecarlo"

FALLBACK_VECTORS = {
    "precharge_equalizer_tran": ["time", "v(eq)", "v(pchg)", "v(bl)", "v(blb)"],
    "peripheral_ic_top_smoke_tran": [
        "time",
        "v(wl_out<0>)",
        "v(col<0>)",
        "v(bl<0>)",
        "v(sense_out<0>)",
    ],
}

SKIP_NAMES = {
    "stack_sram_array_f0",
    "stack_sram_array_f1",
    "stack_sram_array_f2",
    "stack_sram_array_f3",
    "stack_sram_array_f4",
    "stack_sram_array_f5",
    "wl_pad",
    "open3dstack_padframe",
    "open3dstack_user_project_wrapper",
}

SOURCE_BY_NAME = {
    "analog_mux_bl_sl": "analog_mux_bl_sl_nmos.spice",
    "analog_mux_2to1_diff_schematic": "analog_mux_2to1_diff_nmos.spice",
    "analog_mux_2to1_diff": "analog_mux_2to1_diff_nmos.spice",
    "column_decoder": "column_decoder_3to8_nmos.spice",
    "row_decoder": "row_decoder_3to8_nmos.spice",
    "write_driver": "column_driver.spice",
    "opamp": "tb_sense_amp.sp",
    "precharge": "tb_precharge.sp",
    "3d_": "3d_tft_macros.spice",
}

COLORS = ["#0f766e", "#1d4ed8", "#b91c1c", "#9333ea", "#ca8a04", "#334155"]


def parse_eng(value: str | None, default_um: float) -> float:
    if not value:
        return default_um
    token = value.strip().lower().replace("{", "").replace("}", "")
    multipliers = {"u": 1.0, "n": 1e-3, "m": 1e3, "p": 1e-6}
    m = re.fullmatch(r"([-+]?\d*\.?\d+(?:e[-+]?\d+)?)([unmp]?)", token)
    if not m:
        return default_um
    return float(m.group(1)) * multipliers.get(m.group(2), 1e6)


def local_variation(rng: random.Random, w_um: float, l_um: float) -> dict[str, float]:
    area = max(w_um * l_um, 1e-9)
    inv_sqrt_area = 1.0 / math.sqrt(area)
    return {
        "gmis": rng.gauss(0.0, 0.025 + 0.080 * inv_sqrt_area),
        "vmis": rng.gauss(0.0, 0.020 + 0.060 * inv_sqrt_area),
        "wmis": rng.gauss(0.0, 0.010),
        "lmis": rng.gauss(0.0, 0.010),
    }


def passive_variation(rng: random.Random, sigma: float) -> float:
    return rng.gauss(0.0, sigma)


def geometry_from_instance(line: str) -> tuple[float, float]:
    lower = line.lower()
    if "nfet_w20p825_l5" in lower:
        return 20.825, 5.0
    if "nfet_w24u_l5" in lower:
        return 24.0, 5.0
    if "nfet_w6u_l5" in lower:
        return 6.0, 5.0
    w = re.search(r"\bw\s*=\s*([^\s]+)", line, re.I)
    l = re.search(r"\bl\s*=\s*([^\s]+)", line, re.I)
    return parse_eng(w.group(1) if w else None, 8.0), parse_eng(l.group(1) if l else None, 3.0)


def append_local_params(line: str, rng: random.Random) -> str:
    stripped = line.lstrip()
    lower = stripped.lower()
    if not lower.startswith("x") or lower.startswith("xcore"):
        return line
    if " gmis=" in lower:
        return line
    if " nfet_w" not in lower and " tft3d_nfet" not in lower:
        return line
    w_um, l_um = geometry_from_instance(line)
    v = local_variation(rng, w_um, l_um)
    return (
        line.rstrip()
        + f" gmis={v['gmis']:.8g} vmis={v['vmis']:.8g} wmis={v['wmis']:.8g} lmis={v['lmis']:.8g}\n"
    )


def transform_model(text: str, sample: dict[str, float], rng: random.Random, is_3d: bool) -> str:
    header = [
        "* TFT Monte Carlo model include generated for stock ngspice.",
        "* Assumptions: measured conductance table is scaled with W/L and M;",
        "* global process terms shift conductance, Vgs, W, L, internal R, and internal C;",
        "* local mismatch terms are generated per TFT instance with area-aware sigma.",
        f".param mc_gproc={sample['gproc']:.9g}",
        f".param mc_vproc={sample['vproc']:.9g}",
        f".param mc_wproc={sample['wproc']:.9g}",
        f".param mc_lproc={sample['lproc']:.9g}",
        f".param mc_rproc={sample['rproc']:.9g}",
        f".param mc_cproc={sample['cproc']:.9g}",
        "",
    ]

    out: list[str] = []
    for raw in text.splitlines(True):
        line = raw
        low = line.lower()
        if low.startswith(".subckt tft3d_nfet"):
            line = ".subckt tft3d_nfet d g s params: w=8u l=3u m=1 gmis=0 vmis=0 wmis=0 lmis=0\n"
        elif low.startswith("bch d s i={v(d,s)*pwl(((v(s)<v(d)) ? v(g,s) : v(g,d)),"):
            line = "Bch d s I={V(d,s)*(((1+mc_gproc+gmis)>0.05)?(1+mc_gproc+gmis):0.05)*pwl(((V(s)<V(d)) ? V(g,s)+mc_vproc+vmis : V(g,d)+mc_vproc+vmis),\n"
        elif ")*((w/l)/(8u/3u))*m}" in line:
            line = line.replace(")*((w/l)/(8u/3u))*m}", ")*(((w*(1+mc_wproc+wmis))/(l*(1+mc_lproc+lmis)))/(8u/3u))*m}")
        elif low.startswith(".subckt nfet_w") and "gmis=" not in low:
            line = line.rstrip() + " gmis=0 vmis=0 wmis=0 lmis=0\n"
        elif low.lstrip().startswith("xcore") and "tft3d_nfet" in low and "gmis=" not in low:
            line = line.rstrip() + " gmis={gmis} vmis={vmis} wmis={wmis} lmis={lmis}\n"
        elif is_3d and low.startswith("rpu "):
            rv = passive_variation(rng, 0.060)
            line = "RPU VDD Y {24k*(1+mc_rproc" + (f"{rv:+.8g}" if rv else "") + ")}\n"
        elif is_3d and low.startswith("cout "):
            cv = passive_variation(rng, 0.050)
            line = "COUT Y VSS {10f*(1+mc_cproc" + (f"{cv:+.8g}" if cv else "") + ")}\n"
        line = append_local_params(line, rng)
        out.append(line)
    return "\n".join(header) + "".join(out)


def sample_params(rng: random.Random) -> dict[str, float]:
    return {
        "gproc": rng.gauss(0.0, 0.100),
        "vproc": rng.gauss(0.0, 0.070),
        "wproc": rng.gauss(0.0, 0.020),
        "lproc": rng.gauss(0.0, 0.020),
        "rproc": rng.gauss(0.0, 0.120),
        "cproc": rng.gauss(0.0, 0.080),
    }


def parse_ascii_raw(path: Path) -> tuple[list[str], list[list[float]]]:
    lines = path.read_text(errors="replace").splitlines()
    nvars = None
    for line in lines:
        if line.startswith("No. Variables:"):
            nvars = int(line.split(":", 1)[1])
            break
    if nvars is None:
        raise ValueError("missing No. Variables")
    var_start = lines.index("Variables:") + 1
    names = [lines[var_start + i].split()[1] for i in range(nvars)]
    i = lines.index("Values:") + 1
    data: list[list[float]] = []
    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped or stripped.startswith("\f"):
            i += 1
            continue
        parts = stripped.split()
        if len(parts) < 2 or not parts[0].isdigit():
            i += 1
            continue
        values = [float(parts[1])]
        i += 1
        while len(values) < nvars and i < len(lines):
            stripped = lines[i].strip()
            i += 1
            if stripped and not stripped.startswith("\f"):
                values.append(float(stripped.split()[0]))
        if len(values) == nvars:
            data.append(values)
    return names, data


def export_fallback_from_raw(name: str, raw: Path, dat: Path) -> str | None:
    vectors = FALLBACK_VECTORS.get(name)
    if not vectors or not raw.exists():
        return None
    names, data = parse_ascii_raw(raw)
    indices = [names.index(vector) for vector in vectors]
    with dat.open("w") as f:
        f.write(" ".join(vectors) + "\n")
        for row in data:
            f.write(" ".join(f"{row[i]:.12e}" for i in indices) + "\n")
    return "dat extracted from ASCII raw"


def read_dat(path: Path) -> tuple[list[str], list[list[float]]]:
    if not path.exists() or path.stat().st_size == 0:
        return [], []
    lines = path.read_text(errors="replace").splitlines()
    if not lines:
        return [], []
    header = lines[0].split()
    data: list[list[float]] = []
    for line in lines[1:]:
        if not line.strip():
            continue
        try:
            row = [float(token) for token in line.split()]
        except ValueError:
            continue
        if row and all(math.isfinite(x) for x in row):
            data.append(row)
    return header, data


def metric_for(name: str, data: list[list[float]]) -> tuple[str, float, dict[str, float]]:
    if not data or len(data[0]) < 2:
        return "missing", float("nan"), {}
    cols = list(zip(*data))
    stats: dict[str, float] = {"rows": float(len(data))}
    for i, col in enumerate(cols[1:], start=1):
        stats[f"c{i}_min"] = min(col)
        stats[f"c{i}_max"] = max(col)
        stats[f"c{i}_final"] = col[-1]
        stats[f"c{i}_span"] = max(col) - min(col)
    if "idvds" in name or "idvg" in name:
        values = [abs(v) for v in cols[-1]]
        return "max_abs_current", max(values), stats
    if "decoder" in name:
        spans = [max(col) - min(col) for col in cols[3:]] if len(cols) > 3 else [max(cols[-1]) - min(cols[-1])]
        return "decoder_max_swing", max(spans), stats
    if "mux" in name:
        spans = [max(col) - min(col) for col in cols[1:]]
        return "mux_max_swing", max(spans), stats
    if "precharge" in name:
        return "bl_final_delta", abs(cols[-2][-1] - cols[-1][-1]) if len(cols) >= 4 else abs(cols[-1][-1]), stats
    if "opamp" in name:
        return "sense_out_span", max(cols[1]) - min(cols[1]), stats
    if "write_driver" in name:
        spans = [max(col) - min(col) for col in cols[5:]] if len(cols) > 5 else [max(cols[-1]) - min(cols[-1])]
        return "write_node_max_swing", max(spans), stats
    values = cols[-1]
    return "output_span", max(values) - min(values), stats


def source_file_for(name: str) -> str:
    if name.startswith("nfet_"):
        return "generated/native_tft"
    if name.startswith("3d_"):
        return "3d_tft_macros.spice"
    for key, src in SOURCE_BY_NAME.items():
        if key in name:
            return src
    return "peripheral_ic.spice"


def run_one(task: tuple[int, str, str]) -> dict[str, object]:
    sample_idx, deck_path, sample_dir = task
    deck = Path(deck_path)
    sample = Path(sample_dir)
    name = deck.stem
    results = sample / "results"
    dat = results / f"{name}.dat"
    raw = results / f"{name}.raw"
    log = results / f"{name}.log"
    started = time.time()
    try:
        proc = subprocess.run(
            ["ngspice", "-b", "-o", str(log), str(deck)],
            cwd=deck.parent,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=DECK_TIMEOUT_S,
        )
        rc = proc.returncode
    except subprocess.TimeoutExpired as exc:
        rc = 124
        log.write_text((exc.stdout or "") + "\nTIMEOUT\n")
    seconds = round(time.time() - started, 3)
    notes: list[str] = []
    if not dat.exists() or dat.stat().st_size == 0:
        note = export_fallback_from_raw(name, raw, dat)
        if note:
            notes.append(note)
    header, data = read_dat(dat)
    metric_name, metric, stats = metric_for(name, data)
    status = "pass"
    if rc != 0 or not data or not math.isfinite(metric):
        status = "fail"
    elif "id" in metric_name and metric <= 1e-12:
        status = "fail"
    elif "swing" in metric_name and metric <= 1e-6:
        status = "fail"
    if log.exists():
        interesting = [
            line.strip()
            for line in log.read_text(errors="replace").splitlines()
            if re.search(r"(^Error|error|Warning|Fatal|unknown|singular|No\. of Data Rows|TIMEOUT)", line, re.I)
        ]
        notes.extend(interesting[-5:])
    row = {
        "sample": sample_idx,
        "name": name,
        "source_file": source_file_for(name),
        "status": status,
        "rc": rc,
        "seconds": seconds,
        "rows": len(data),
        "metric_name": metric_name,
        "metric": metric,
        "dat": str(dat),
        "raw": str(raw) if raw.exists() else "",
        "log": str(log) if log.exists() else "",
        "notes": " | ".join(notes)[:1200],
    }
    row.update(stats)
    return row


def write_hist_svg(values: list[float], out: Path, title: str) -> None:
    vals = [v for v in values if math.isfinite(v)]
    if not vals:
        return
    width, height = 760, 420
    left, right, top, bottom = 70, 25, 45, 55
    vmin, vmax = min(vals), max(vals)
    if math.isclose(vmin, vmax):
        vmin -= abs(vmin) * 0.05 + 1e-12
        vmax += abs(vmax) * 0.05 + 1e-12
    bins = 16
    counts = [0] * bins
    for v in vals:
        idx = min(bins - 1, max(0, int((v - vmin) / (vmax - vmin) * bins)))
        counts[idx] += 1
    maxc = max(counts) or 1
    def sx(i: int) -> float:
        return left + i / bins * (width - left - right)
    def sy(c: int) -> float:
        return height - bottom - c / maxc * (height - top - bottom)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width/2}" y="28" text-anchor="middle" font-family="Arial" font-size="18">{title}</text>',
        f'<line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" stroke="#111827"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" stroke="#111827"/>',
    ]
    for i, c in enumerate(counts):
        x0, x1 = sx(i), sx(i + 1) - 2
        y = sy(c)
        parts.append(f'<rect x="{x0:.1f}" y="{y:.1f}" width="{max(1, x1-x0):.1f}" height="{height-bottom-y:.1f}" fill="{COLORS[i % len(COLORS)]}" opacity="0.82"/>')
    parts.append(f'<text x="{left}" y="{height-18}" font-family="Arial" font-size="12">min {vmin:.4g}</text>')
    parts.append(f'<text x="{width-right}" y="{height-18}" text-anchor="end" font-family="Arial" font-size="12">max {vmax:.4g}</text>')
    parts.append('</svg>')
    out.write_text("\n".join(parts) + "\n")


def aggregate(records: list[dict[str, object]], out_root: Path, variations: list[dict[str, float]], sample_count: int, seed: int) -> None:
    results = out_root / "results"
    plots = out_root / "plots"
    results.mkdir(parents=True, exist_ok=True)
    plots.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({k for r in records for k in r.keys()}, key=lambda x: (x not in ["sample", "name", "status", "metric", "metric_name"], x))
    with (results / "summary.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)
    (results / "summary.json").write_text(json.dumps(records, indent=2) + "\n")
    with (results / "variation_manifest.csv").open("w", newline="") as f:
        cols = ["sample", "gproc", "vproc", "wproc", "lproc", "rproc", "cproc"]
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        writer.writerows(variations)

    decks = sorted({str(r["name"]) for r in records})
    agg_rows = []
    for name in decks:
        rs = [r for r in records if r["name"] == name]
        vals = [float(r["metric"]) for r in rs if r["status"] == "pass" and math.isfinite(float(r["metric"]))]
        if vals:
            mean = sum(vals) / len(vals)
            std = math.sqrt(sum((v - mean) ** 2 for v in vals) / len(vals))
            minv, maxv = min(vals), max(vals)
        else:
            mean = std = minv = maxv = float("nan")
        agg_rows.append({
            "name": name,
            "source_file": source_file_for(name),
            "samples": len(rs),
            "pass": sum(1 for r in rs if r["status"] == "pass"),
            "fail": sum(1 for r in rs if r["status"] != "pass"),
            "metric_name": rs[0].get("metric_name", "") if rs else "",
            "mean": mean,
            "std": std,
            "min": minv,
            "max": maxv,
        })
        write_hist_svg(vals, plots / f"{name}_metric_hist.svg", name)
    with (results / "aggregate.csv").open("w", newline="") as f:
        cols = ["name", "source_file", "samples", "pass", "fail", "metric_name", "mean", "std", "min", "max"]
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        writer.writerows(agg_rows)

    failures = [r for r in records if r["status"] != "pass"]
    with (results / "failures.csv").open("w", newline="") as f:
        cols = ["sample", "name", "status", "rc", "rows", "metric_name", "metric", "notes", "log"]
        writer = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(failures)

    pass_total = sum(1 for r in records if r["status"] == "pass")
    fail_total = len(records) - pass_total
    lines = [
        "# TFT ngspice Monte Carlo verification report",
        "",
        f"Samples: {sample_count}",
        f"Decks per sample: {len(decks)}",
        f"Total ngspice runs: {len(records)}",
        f"Pass: {pass_total}",
        f"Fail: {fail_total}",
        f"Seed: {seed}",
        "",
        "## Variation Model",
        "",
        "- Global process terms: conductance scale, Vgs offset, W bias, L bias, internal R bias, internal C bias.",
        "- Local TFT mismatch terms: conductance, Vgs offset, W, and L perturbations generated per device instance.",
        "- Local conductance/Vgs mismatch sigma scales with 1/sqrt(W*L) in square microns.",
        "- This is a Monte Carlo stress model for the measured-table TFT abstraction, not a silicon-qualified statistical model.",
        "",
        "## Aggregate Results",
        "",
    ]
    for row in agg_rows:
        lines.append(
            f"- `{row['name']}`: pass {row['pass']}/{row['samples']}, "
            f"{row['metric_name']} mean={row['mean']:.5g}, std={row['std']:.5g}, "
            f"min={row['min']:.5g}, max={row['max']:.5g}"
        )
    lines += ["", "## Failure Summary", ""]
    if failures:
        for r in failures[:100]:
            lines.append(f"- sample {r['sample']} `{r['name']}` rc={r['rc']} notes={r.get('notes','')}")
    else:
        lines.append("- none")
    lines += ["", "## Files", "", "- `results/summary.csv`", "- `results/aggregate.csv`", "- `results/variation_manifest.csv`", "- `results/failures.csv`", "- `plots/*_metric_hist.svg`"]
    (results / "REPORT.md").write_text("\n".join(lines) + "\n")


def prepare(args: argparse.Namespace) -> tuple[Path, list[Path], list[dict[str, float]]]:
    root = Path(args.root).expanduser().resolve()
    base = Path(args.base).expanduser().resolve()
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    (root / "samples").mkdir()
    (root / "results").mkdir()
    (root / "plots").mkdir()
    tb_src = base / "tb"
    model_main = (base / "models" / "lib_main_clean.spice").read_text()
    model_3d = (base / "models" / "lib_3d_tft_macros_clean.spice").read_text()
    decks = sorted(tb_src.glob("*.cir"))
    rng = random.Random(args.seed)
    variations: list[dict[str, float]] = []
    for sample_idx in range(args.samples):
        sample_dir = root / "samples" / f"s{sample_idx:03d}"
        (sample_dir / "tb").mkdir(parents=True)
        (sample_dir / "models").mkdir()
        (sample_dir / "results").mkdir()
        params = sample_params(rng)
        variations.append({"sample": sample_idx, **params})
        # Use separate RNG streams so model-instance mismatch is reproducible per sample and per library.
        rng_main = random.Random(args.seed * 1000003 + sample_idx * 17 + 1)
        rng_3d = random.Random(args.seed * 1000003 + sample_idx * 17 + 2)
        (sample_dir / "models" / "lib_main_clean.spice").write_text(transform_model(model_main, params, rng_main, False))
        (sample_dir / "models" / "lib_3d_tft_macros_clean.spice").write_text(transform_model(model_3d, params, rng_3d, True))
        for deck in decks:
            shutil.copy2(deck, sample_dir / "tb" / deck.name)
    (root / "README.md").write_text(
        "# TFT ngspice Monte Carlo run\n\n"
        "Generated by `scripts/run_montecarlo.py` from the existing `tb/` and `models/` folders.\n"
        "Generated artifacts are under `samples/`, `results/`, and `plots/`.\n"
    )
    return root, decks, variations


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default=str(ROOT), help="NG_spice_macros directory containing tb/ and models/.")
    parser.add_argument("--root", default=str(DEFAULT_OUTPUT), help="Output directory for generated samples/results/plots.")
    parser.add_argument("--samples", type=int, default=64)
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--seed", type=int, default=SEED_DEFAULT)
    args = parser.parse_args()

    work_root, _decks, variations = prepare(args)
    tasks: list[tuple[int, str, str]] = []
    for sample_idx in range(args.samples):
        sample_dir = work_root / "samples" / f"s{sample_idx:03d}"
        for deck in sorted((sample_dir / "tb").glob("*.cir")):
            tasks.append((sample_idx, str(deck), str(sample_dir)))
    started = time.time()
    records: list[dict[str, object]] = []
    with ProcessPoolExecutor(max_workers=args.jobs) as ex:
        futures = [ex.submit(run_one, task) for task in tasks]
        done = 0
        total = len(futures)
        for fut in as_completed(futures):
            records.append(fut.result())
            done += 1
            if done % 50 == 0 or done == total:
                print(f"completed {done}/{total}", flush=True)
    records.sort(key=lambda r: (int(r["sample"]), str(r["name"])))
    aggregate(records, work_root, variations, args.samples, args.seed)
    elapsed = time.time() - started
    pass_total = sum(1 for r in records if r["status"] == "pass")
    fail_total = len(records) - pass_total
    print(f"MC_DONE samples={args.samples} runs={len(records)} pass={pass_total} fail={fail_total} seconds={elapsed:.1f}")
    return 0 if fail_total == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
