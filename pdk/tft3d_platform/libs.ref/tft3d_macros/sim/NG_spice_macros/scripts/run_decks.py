#!/usr/bin/env python3
from __future__ import annotations

import csv
import html
import json
import math
import re
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TB_DIR = ROOT / "tb"
RESULTS_DIR = ROOT / "results"
PLOTS_DIR = ROOT / "plots"

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

SKIPPED = [
    "stack_sram_array_f0",
    "stack_sram_array_f1",
    "stack_sram_array_f2",
    "stack_sram_array_f3",
    "stack_sram_array_f4",
    "stack_sram_array_f5",
    "wl_pad",
    "open3dstack_padframe",
    "open3dstack_user_project_wrapper",
]

SOURCE_BY_NAME = {
    "analog_mux_bl_sl": "analog_mux_bl_sl_nmos.spice",
    "analog_mux": "analog_mux_2to1_diff_nmos.spice",
    "column_decoder": "column_decoder_3to8_nmos.spice",
    "row_decoder": "row_decoder_3to8_nmos.spice",
    "write_driver": "column_driver.spice",
    "opamp": "tb_sense_amp.sp",
    "precharge": "tb_precharge.sp",
    "3d_": "3d_tft_macros.spice",
}

COLORS = [
    "#0f766e",
    "#b91c1c",
    "#1d4ed8",
    "#9333ea",
    "#ca8a04",
    "#0f172a",
    "#be185d",
    "#15803d",
    "#ea580c",
    "#0891b2",
    "#4f46e5",
    "#7c2d12",
]


def source_file_for(name: str) -> str:
    if name.startswith("nfet_"):
        return "generated/native_tft"
    if name.startswith("3d_"):
        return "3d_tft_macros.spice"
    for key, source in SOURCE_BY_NAME.items():
        if key in name:
            return source
    return "peripheral_ic.spice"


def category_for(name: str) -> str:
    if name.startswith("nfet_") or "_nfet_" in name:
        return "primitive_dc"
    if name.startswith("3d_"):
        return "3d_macro"
    if "decoder" in name:
        return "decoder_tran"
    if "mux" in name:
        return "mux_tran"
    if "write_driver" in name:
        return "write_tran"
    if "precharge" in name:
        return "precharge_tran"
    if "opamp" in name:
        return "sense_tran"
    if name.startswith("wl_"):
        return "wl"
    if "top_smoke" in name:
        return "top_smoke"
    return "logic"


def parse_ascii_raw(path: Path) -> tuple[list[str], list[list[float]]]:
    lines = path.read_text(errors="replace").splitlines()
    nvars = None
    for line in lines:
        if line.startswith("No. Variables:"):
            nvars = int(line.split(":", 1)[1])
            break
    if nvars is None:
        raise ValueError(f"{path}: missing No. Variables")

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
            if not stripped or stripped.startswith("\f"):
                continue
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
            f.write(" ".join(f"{row[index]:.12e}" for index in indices) + "\n")
    return "dat extracted from ASCII raw because ngspice-36 wrdata rejected this vector expression"


def read_dat(path: Path) -> tuple[list[str], list[list[float]]]:
    lines = path.read_text(errors="replace").splitlines()
    if not lines:
        return [], []
    header = lines[0].split()
    data: list[list[float]] = []
    for line in lines[1:]:
        if not line.strip():
            continue
        try:
            data.append([float(token) for token in line.split()])
        except ValueError:
            continue
    return header, data


def fmt(value: float) -> str:
    if abs(value) >= 1e3 or (value != 0 and abs(value) < 1e-2):
        return f"{value:.2e}"
    return f"{value:.3g}"


def write_svg(dat: Path, out: Path, title: str, y_scale: float = 1.0, max_cols: int = 8) -> bool:
    header, data = read_dat(dat)
    if not data or len(data[0]) < 2:
        return False

    ncols = min(len(data[0]), max_cols + 1)
    x = [row[0] for row in data]
    ys = [[row[i] * y_scale for row in data] for i in range(1, ncols)]
    labels = header[1:ncols] if len(header) >= ncols else [f"y{i}" for i in range(1, ncols)]

    xmin, xmax = min(x), max(x)
    ymin, ymax = min(min(y) for y in ys), max(max(y) for y in ys)
    if math.isclose(xmin, xmax):
        xmax = xmin + 1.0
    if math.isclose(ymin, ymax):
        ymin -= 1.0
        ymax += 1.0
    pad = (ymax - ymin) * 0.08
    ymin -= pad
    ymax += pad

    width, height = 960, 560
    left, right, top, bottom = 80, 30, 50, 80

    def sx(value: float) -> float:
        return left + (value - xmin) / (xmax - xmin) * (width - left - right)

    def sy(value: float) -> float:
        return height - bottom - (value - ymin) / (ymax - ymin) * (height - top - bottom)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width/2}" y="28" text-anchor="middle" font-family="Arial" font-size="22">{html.escape(title)}</text>',
    ]

    for k in range(6):
        xv = xmin + (xmax - xmin) * k / 5
        yv = ymin + (ymax - ymin) * k / 5
        px, py = sx(xv), sy(yv)
        parts.append(f'<line x1="{px:.1f}" y1="{top}" x2="{px:.1f}" y2="{height-bottom}" stroke="#e5e7eb"/>')
        parts.append(f'<text x="{px:.1f}" y="{height-bottom+24}" text-anchor="middle" font-family="Arial" font-size="12">{fmt(xv)}</text>')
        parts.append(f'<line x1="{left}" y1="{py:.1f}" x2="{width-right}" y2="{py:.1f}" stroke="#e5e7eb"/>')
        parts.append(f'<text x="{left-10}" y="{py+4:.1f}" text-anchor="end" font-family="Arial" font-size="12">{fmt(yv)}</text>')

    parts.append(f'<line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" stroke="#111827"/>')
    parts.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" stroke="#111827"/>')

    for i, y in enumerate(ys):
        color = COLORS[i % len(COLORS)]
        points = " ".join(f"{sx(xx):.2f},{sy(yy):.2f}" for xx, yy in zip(x, y))
        parts.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2"/>')
        lx = left + 12 + (i % 4) * 210
        ly = height - 38 + (i // 4) * 18
        parts.append(f'<line x1="{lx}" y1="{ly}" x2="{lx+28}" y2="{ly}" stroke="{color}" stroke-width="3"/>')
        parts.append(f'<text x="{lx+36}" y="{ly+4}" font-family="Arial" font-size="12">{html.escape(labels[i])}</text>')

    parts.append("</svg>")
    out.write_text("\n".join(parts) + "\n")
    return True


def write_idvds_overlay(records: list[dict[str, object]]) -> None:
    selected = ["nfet_w6u_l5_idvds_vg3", "nfet_w20p825_l5_idvds_vg3", "nfet_w24u_l5_idvds_vg3"]
    series = []
    for name in selected:
        dat = RESULTS_DIR / f"{name}.dat"
        _, data = read_dat(dat) if dat.exists() else ([], [])
        if data:
            series.append((name, [row[0] for row in data], [row[1] * 1e6 for row in data]))
    if not series:
        return

    tmp = RESULTS_DIR / ".nfet_family_overlay.tmp.dat"
    with tmp.open("w") as f:
        f.write("vds " + " ".join(name.replace("_idvds_vg3", "") for name in selected) + "\n")
        for i in range(min(len(s[1]) for s in series)):
            f.write(" ".join([f"{series[0][1][i]:.12e}"] + [f"{s[2][i]:.12e}" for s in series]) + "\n")
    write_svg(tmp, PLOTS_DIR / "nfet_family_idvds_overlay.svg", "Parameterized TFT family Id-Vds, Vg=3V (uA)")
    tmp.unlink(missing_ok=True)


def write_report(records: list[dict[str, object]]) -> None:
    passes = [r for r in records if r.get("status") == "pass"]
    fails = [r for r in records if r.get("status") == "fail"]
    skipped = [r for r in records if str(r.get("status", "")).startswith("skipped")]

    with (RESULTS_DIR / "summary.csv").open("w", newline="") as f:
        cols = ["name", "category", "source_file", "status", "rc", "seconds", "data_rows", "dat", "raw", "log", "notes"]
        writer = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)

    (RESULTS_DIR / "summary.json").write_text(json.dumps(records, indent=2) + "\n")

    lines = [
        "# NG-spice macro simulation report",
        "",
        "Run this suite from `pdk/tft3d_platform/libs.ref/tft3d_macros/sim/NG_spice_macros` with `./run_all.sh`.",
        "",
        f"Pass: {len(passes)}",
        f"Fail: {len(fails)}",
        f"Skipped physical/empty: {len(skipped)}",
        "",
        "## Passed Decks",
    ]
    for r in passes:
        lines.append(f"- `{r['name']}` ({r.get('source_file', '')}) rows={r.get('data_rows')} dat=`{r.get('dat')}`")
    lines.extend(["", "## Failed Decks"])
    if fails:
        for r in fails:
            lines.append(f"- `{r['name']}` rc={r.get('rc')} notes={r.get('notes', '')}")
    else:
        lines.append("- none")
    lines.extend(["", "## Skipped"])
    for r in skipped:
        lines.append(f"- `{r['name']}`: {r.get('notes', '')}")
    lines.extend(["", "## Plot Files"])
    for plot in sorted(PLOTS_DIR.glob("*.svg")):
        lines.append(f"- `{plot.relative_to(ROOT)}`")
    (RESULTS_DIR / "REPORT.md").write_text("\n".join(lines) + "\n")


def main() -> int:
    RESULTS_DIR.mkdir(exist_ok=True)
    PLOTS_DIR.mkdir(exist_ok=True)
    for pattern in ("*.dat", "*.raw", "*.log", "summary.csv", "summary.json", "REPORT.md"):
        for old in RESULTS_DIR.glob(pattern):
            old.unlink()
    for old in PLOTS_DIR.glob("*.svg"):
        old.unlink()

    records: list[dict[str, object]] = []
    for deck in sorted(TB_DIR.glob("*.cir")):
        name = deck.stem
        dat = RESULTS_DIR / f"{name}.dat"
        raw = RESULTS_DIR / f"{name}.raw"
        log = RESULTS_DIR / f"{name}.log"
        started = time.time()
        try:
            proc = subprocess.run(
                ["ngspice", "-b", "-o", str(log), str(deck)],
                cwd=TB_DIR,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=180,
            )
            rc = proc.returncode
        except subprocess.TimeoutExpired as exc:
            rc = 124
            log.write_text((exc.stdout or "") + "\nTIMEOUT\n")
        seconds = round(time.time() - started, 3)

        notes: list[str] = []
        if not dat.exists() or dat.stat().st_size == 0:
            fallback_note = export_fallback_from_raw(name, raw, dat)
            if fallback_note:
                notes.append(fallback_note)

        data_rows = max(0, len(dat.read_text(errors="replace").splitlines()) - 1) if dat.exists() else 0
        status = "pass" if rc == 0 and data_rows > 0 else "fail"
        if log.exists():
            interesting = [
                line.strip()
                for line in log.read_text(errors="replace").splitlines()
                if re.search(r"(^Error|error|Warning|Fatal|unknown|singular|No\\. of Data Rows)", line, re.I)
            ]
            notes.extend(interesting[-4:])

        title = name
        y_scale = 1e6 if ("idvds" in name or "idvg" in name) else 1.0
        if y_scale != 1.0:
            title += " (current in uA)"
        if status == "pass":
            write_svg(dat, PLOTS_DIR / f"{name}.svg", title, y_scale=y_scale)

        records.append(
            {
                "name": name,
                "category": category_for(name),
                "source_file": source_file_for(name),
                "status": status,
                "rc": rc,
                "seconds": seconds,
                "data_rows": data_rows,
                "dat": str(dat.relative_to(ROOT)) if dat.exists() else "",
                "raw": str(raw.relative_to(ROOT)) if raw.exists() else "",
                "log": str(log.relative_to(ROOT)) if log.exists() else "",
                "notes": " | ".join(notes)[:1000],
            }
        )

    for name in SKIPPED:
        records.append(
            {
                "name": name,
                "status": "skipped_no_devices_or_physical_only",
                "notes": "Subckt is empty/physical-only in source netlist; no meaningful electrical output to plot.",
            }
        )

    write_idvds_overlay(records)
    write_report(records)

    passes = sum(1 for r in records if r.get("status") == "pass")
    fails = sum(1 for r in records if r.get("status") == "fail")
    skipped = sum(1 for r in records if str(r.get("status", "")).startswith("skipped"))
    print(f"pass={passes} fail={fails} skipped={skipped} plots={len(list(PLOTS_DIR.glob('*.svg')))}")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
