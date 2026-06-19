#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import os
import re
import shutil
from pathlib import Path


SIM_ROOT = Path(__file__).resolve().parents[1]
MACRO_ROOT = SIM_ROOT.parents[1]
CDSLIB_ROOT = MACRO_ROOT / "cdslib"
LIB_ROOT = CDSLIB_ROOT / "tft3d_macros"


CELLS = [
    {
        "cell": "INV_X4PC_T5_nmos",
        "subckt": "INV_X4PC_T5_nmos",
        "deck": "3d_inv_x4pc_transfer",
        "model": "models/lib_3d_tft_macros_clean.spice",
        "source": "spice/3d_tft_macros.spice",
    },
    {
        "cell": "NAND3_X4RL_T5",
        "subckt": "NAND3_X4RL_T5",
        "deck": "3d_nand3_x4rl_transfer_a1",
        "model": "models/lib_3d_tft_macros_clean.spice",
        "source": "spice/3d_tft_macros.spice",
    },
    {
        "cell": "analog_mux_bl_sl_pitch260",
        "subckt": "analog_mux_bl_sl_nmos",
        "deck": "analog_mux_bl_sl_tran",
        "model": "models/lib_main_clean.spice",
        "source": "spice/analog_mux_bl_sl_nmos.spice",
    },
    {
        "cell": "column_decoder_3to8_nmos_vertical_pitch260",
        "subckt": "column_decoder_3to8_nmos",
        "deck": "column_decoder_3to8_tran",
        "model": "models/lib_main_clean.spice",
        "source": "spice/column_decoder_3to8_nmos.spice",
    },
    {
        "cell": "column_driver_vertical_pitch260",
        "subckt": "write_driver",
        "deck": "write_driver_tran",
        "model": "models/lib_main_clean.spice",
        "source": "spice/column_driver.spice",
    },
    {
        "cell": "nfet_W20p825_L5",
        "subckt": "nfet_W20p825_L5",
        "deck": "3d_nfet_W20p825_L5_idvds_vg3",
        "model": "models/lib_3d_tft_macros_clean.spice",
        "source": "spice/3d_tft_macros.spice",
    },
    {
        "cell": "nfet_W24u_L5",
        "subckt": "nfet_W24u_L5",
        "deck": "3d_nfet_W24u_L5_idvds_vg3",
        "model": "models/lib_3d_tft_macros_clean.spice",
        "source": "spice/3d_tft_macros.spice",
    },
    {
        "cell": "nfet_W6u_L5",
        "subckt": "nfet_W6u_L5",
        "deck": "3d_nfet_W6u_L5_idvds_vg3",
        "model": "models/lib_3d_tft_macros_clean.spice",
        "source": "spice/3d_tft_macros.spice",
    },
    {
        "cell": "precharge_equalizer_nmos_6u_pitch260",
        "subckt": "precharge_equalizer_nmos_6u",
        "deck": "precharge_equalizer_tran",
        "model": "models/lib_main_clean.spice",
        "source": "spice/tb_precharge.sp",
    },
    {
        "cell": "row_decoder_3to8_nmos",
        "subckt": "row_decoder_3to8_nmos",
        "deck": "row_decoder_3to8_tran",
        "model": "models/lib_main_clean.spice",
        "source": "spice/row_decoder_3to8_nmos.spice",
    },
    {
        "cell": "sense_amp_sl_slb_pitch260",
        "subckt": "opamp_6u",
        "deck": "opamp_6u_sense_tran",
        "model": "models/lib_main_clean.spice",
        "source": "spice/tb_sense_amp.sp",
    },
    {
        "cell": "wl_inv",
        "subckt": "wl_inv",
        "deck": "3d_wl_inv_transfer",
        "model": "models/lib_3d_tft_macros_clean.spice",
        "source": "spice/3d_tft_macros.spice",
    },
    {
        "cell": "wl_prebuffer",
        "subckt": "wl_prebuffer",
        "deck": "3d_wl_prebuffer_transfer",
        "model": "models/lib_3d_tft_macros_clean.spice",
        "source": "spice/3d_tft_macros.spice",
    },
    {
        "cell": "wl_sel",
        "subckt": "wl_sel",
        "deck": "3d_wl_sel_transfer",
        "model": "models/lib_3d_tft_macros_clean.spice",
        "source": "spice/3d_tft_macros.spice",
    },
]


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def rel(path: Path) -> str:
    return path.relative_to(MACRO_ROOT).as_posix()


def link(target: Path, link_path: Path) -> None:
    link_path.parent.mkdir(parents=True, exist_ok=True)
    if link_path.exists() or link_path.is_symlink():
        link_path.unlink()
    link_path.symlink_to(os.path.relpath(target, link_path.parent))


def subckt_pins(model_rel: str, subckt: str) -> list[str]:
    model_path = SIM_ROOT / model_rel
    pattern = re.compile(rf"^\.subckt\s+{re.escape(subckt)}\s+(.*)$", re.IGNORECASE)
    for line in model_path.read_text(errors="replace").splitlines():
        match = pattern.match(line.strip())
        if match:
            return [token for token in match.group(1).split() if not token.lower().startswith("params:")]
    return []


def symbol_svg(cell: str, pins: list[str]) -> str:
    height = max(180, 90 + 18 * max(1, len(pins)))
    body_top = 40
    body_height = height - 80
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="520" height="{height}" viewBox="0 0 520 {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<rect x="150" y="{body_top}" width="220" height="{body_height}" fill="#f8fafc" stroke="#111827" stroke-width="2"/>',
        f'<text x="260" y="{body_top + 30}" text-anchor="middle" font-family="Arial" font-size="16" font-weight="700">{cell}</text>',
    ]
    left = pins[: (len(pins) + 1) // 2]
    right = pins[(len(pins) + 1) // 2 :]
    for side, side_pins in (("left", left), ("right", right)):
        step = body_height / (len(side_pins) + 1) if side_pins else body_height / 2
        for index, pin in enumerate(side_pins, start=1):
            y = body_top + step * index
            if side == "left":
                parts.append(f'<line x1="90" y1="{y:.1f}" x2="150" y2="{y:.1f}" stroke="#111827"/>')
                parts.append(f'<text x="84" y="{y + 4:.1f}" text-anchor="end" font-family="Arial" font-size="12">{pin}</text>')
            else:
                parts.append(f'<line x1="370" y1="{y:.1f}" x2="430" y2="{y:.1f}" stroke="#111827"/>')
                parts.append(f'<text x="436" y="{y + 4:.1f}" font-family="Arial" font-size="12">{pin}</text>')
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> int:
    if CDSLIB_ROOT.exists():
        shutil.rmtree(CDSLIB_ROOT)
    LIB_ROOT.mkdir(parents=True)

    write(CDSLIB_ROOT / "cds.lib", "DEFINE tft3d_macros ./tft3d_macros\n")
    write(
        CDSLIB_ROOT / "README.md",
        "# tft3d_macros Cadence-style ngspice library\n\n"
        "Generated by `sim/NG_spice_macros/scripts/build_cdslib.py`.\n"
        "Only cells with real non-smoke NGspice coverage are included.\n",
    )
    write(LIB_ROOT / "data.dm", "# Generated library marker\n")
    write(LIB_ROOT / "cdsinfo.tag", "generated library\n")

    rows = []
    for item in CELLS:
        cell = item["cell"]
        deck = item["deck"]
        cell_dir = LIB_ROOT / cell
        pins = subckt_pins(item["model"], item["subckt"])
        gds = MACRO_ROOT / "gds" / f"{cell}.gds"
        lef = MACRO_ROOT / "lef" / f"{cell}.lef"
        tb = SIM_ROOT / "tb" / f"{deck}.cir"
        dat = SIM_ROOT / "results" / f"{deck}.dat"
        plot = SIM_ROOT / "plots" / f"{deck}.svg"

        for view in ("layout", "abstract", "symbol", "schematic", "simulation"):
            write(cell_dir / view / "data.dm", f"# Generated {view} view for {cell}\n")

        link(gds, cell_dir / "layout" / "layout.gds")
        if lef.exists():
            link(lef, cell_dir / "abstract" / "abstract.lef")
        link(tb, cell_dir / "schematic" / "ngspice.cir")
        link(SIM_ROOT / item["model"], cell_dir / "schematic" / "model.spice")
        source = MACRO_ROOT / item["source"]
        if source.exists():
            link(source, cell_dir / "schematic" / "source.spice")
        link(dat, cell_dir / "simulation" / "results.dat")
        link(plot, cell_dir / "simulation" / "plot.svg")

        write(cell_dir / "symbol" / "symbol.svg", symbol_svg(cell, pins))
        write(cell_dir / "symbol" / "symbol.json", json.dumps({"cell": cell, "pins": pins}, indent=2) + "\n")
        write(
            cell_dir / "cell.json",
            json.dumps(
                {
                    "library": "tft3d_macros",
                    "cell": cell,
                    "subckt": item["subckt"],
                    "primary_deck": deck,
                    "layout": rel(gds),
                    "schematic": rel(tb),
                    "simulation": rel(dat),
                    "plot": rel(plot),
                    "pins": pins,
                },
                indent=2,
            )
            + "\n",
        )
        rows.append(
            {
                "cell": cell,
                "gds": rel(gds),
                "subckt": item["subckt"],
                "primary_deck": deck,
                "testbench": rel(tb),
                "results": rel(dat),
                "plot": rel(plot),
            }
        )

    with (LIB_ROOT / "cells.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["cell", "gds", "subckt", "primary_deck", "testbench", "results", "plot"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"cdslib_cells={len(rows)} cdslib={CDSLIB_ROOT.relative_to(MACRO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
