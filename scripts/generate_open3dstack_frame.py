#!/usr/bin/env python3
"""Generate the Open3DStack pad-only frame views.

The frame is intentionally Caravel-like in artifact shape, but it contains only
the pad ring and an empty user-project wrapper area.  The source pad primitive
is wl_pad.gds.
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

import gdstk


ROOT = Path(__file__).resolve().parents[1]
MACRO_LIB = ROOT / "pdk/tft3d_platform/libs.ref/tft3d_macros"
PAD_GDS = MACRO_LIB / "gds/wl_pad.gds"

DIE_W = 25_000.0
DIE_H = 22_000.0
USER_X0 = 1_000.0
USER_Y0 = 1_000.0
USER_W = 23_000.0
USER_H = 20_000.0

PAD_W = 100.0
PAD_H = 130.0
PAD_MARGIN = 500.0
PAD_PITCH = 500.0

PIN_LAYER = "SD"


@dataclass(frozen=True)
class Pad:
    name: str
    index: int
    side: str
    center_x: float
    center_y: float
    origin_x: float
    origin_y: float
    rotation_deg: int
    bbox: tuple[float, float, float, float]
    user_pin_bbox: tuple[float, float, float, float]
    default_kind: str = "analog"


def fmt(value: float) -> str:
    return f"{value:.3f}".rstrip("0").rstrip(".")


def side_positions(start: float, stop: float, pitch: float) -> list[float]:
    count = int(round((stop - start) / pitch)) + 1
    return [start + i * pitch for i in range(count)]


def make_pads() -> list[Pad]:
    pads: list[Pad] = []
    x_positions = side_positions(PAD_MARGIN, DIE_W - PAD_MARGIN, PAD_PITCH)
    y_positions = side_positions(PAD_MARGIN, DIE_H - PAD_MARGIN, PAD_PITCH)

    def user_pin_for_side(side: str, idx: int, count: int) -> tuple[float, float, float, float]:
        pitch_x = USER_W / (count + 1)
        pitch_y = USER_H / (count + 1)
        pin = 20.0
        if side == "N":
            x = pitch_x * (idx + 1)
            return (x - pin / 2, USER_H - pin, x + pin / 2, USER_H)
        if side == "S":
            x = pitch_x * (idx + 1)
            return (x - pin / 2, 0.0, x + pin / 2, pin)
        if side == "E":
            y = pitch_y * (idx + 1)
            return (USER_W - pin, y - pin / 2, USER_W, y + pin / 2)
        if side == "W":
            y = pitch_y * (idx + 1)
            return (0.0, y - pin / 2, pin, y + pin / 2)
        raise ValueError(side)

    for i, x in enumerate(x_positions):
        pads.append(
            Pad(
                name=f"PAD_S{i:02d}",
                index=len(pads),
                side="S",
                center_x=x,
                center_y=PAD_H / 2,
                origin_x=x - PAD_W / 2,
                origin_y=0.0,
                rotation_deg=0,
                bbox=(x - PAD_W / 2, 0.0, x + PAD_W / 2, PAD_H),
                user_pin_bbox=user_pin_for_side("S", i, len(x_positions)),
            )
        )
    for i, y in enumerate(y_positions):
        pads.append(
            Pad(
                name=f"PAD_E{i:02d}",
                index=len(pads),
                side="E",
                center_x=DIE_W - PAD_H / 2,
                center_y=y,
                origin_x=DIE_W - PAD_H,
                origin_y=y + PAD_W / 2,
                rotation_deg=270,
                bbox=(DIE_W - PAD_H, y - PAD_W / 2, DIE_W, y + PAD_W / 2),
                user_pin_bbox=user_pin_for_side("E", i, len(y_positions)),
            )
        )
    for i, x in enumerate(x_positions):
        pads.append(
            Pad(
                name=f"PAD_N{i:02d}",
                index=len(pads),
                side="N",
                center_x=x,
                center_y=DIE_H - PAD_H / 2,
                origin_x=x + PAD_W / 2,
                origin_y=DIE_H,
                rotation_deg=180,
                bbox=(x - PAD_W / 2, DIE_H - PAD_H, x + PAD_W / 2, DIE_H),
                user_pin_bbox=user_pin_for_side("N", i, len(x_positions)),
            )
        )
    for i, y in enumerate(y_positions):
        pads.append(
            Pad(
                name=f"PAD_W{i:02d}",
                index=len(pads),
                side="W",
                center_x=PAD_H / 2,
                center_y=y,
                origin_x=PAD_H,
                origin_y=y - PAD_W / 2,
                rotation_deg=90,
                bbox=(0.0, y - PAD_W / 2, PAD_H, y + PAD_W / 2),
                user_pin_bbox=user_pin_for_side("W", i, len(y_positions)),
            )
        )
    return pads


def add_outline(cell: gdstk.Cell, x0: float, y0: float, x1: float, y1: float, width: float, layer: int, datatype: int) -> None:
    cell.add(gdstk.rectangle((x0, y0), (x1, y0 + width), layer=layer, datatype=datatype))
    cell.add(gdstk.rectangle((x0, y1 - width), (x1, y1), layer=layer, datatype=datatype))
    cell.add(gdstk.rectangle((x0, y0), (x0 + width, y1), layer=layer, datatype=datatype))
    cell.add(gdstk.rectangle((x1 - width, y0), (x1, y1), layer=layer, datatype=datatype))


def copy_pad_geometry(target: gdstk.Cell, pad_cell: gdstk.Cell, pad: Pad) -> None:
    angle = math.radians(pad.rotation_deg)
    for poly in pad_cell.polygons:
        copied = poly.copy()
        if pad.rotation_deg:
            copied.rotate(angle)
        copied.translate(pad.origin_x, pad.origin_y)
        target.add(copied)
    target.add(gdstk.Label(pad.name, (pad.center_x, pad.center_y), anchor="o", rotation=angle, layer=54, texttype=3))


def generate_gds(pads: list[Pad]) -> None:
    source = gdstk.read_gds(str(PAD_GDS))
    pad_cell = next(cell for cell in source.cells if cell.name == "wl_pad")

    lib = gdstk.Library(unit=source.unit, precision=source.precision)
    frame = lib.new_cell("open3dstack_padframe")
    for pad in pads:
        copy_pad_geometry(frame, pad_cell, pad)

    add_outline(frame, 0.0, 0.0, DIE_W, DIE_H, 10.0, 150, 5)
    add_outline(frame, USER_X0, USER_Y0, USER_X0 + USER_W, USER_Y0 + USER_H, 20.0, 152, 5)

    lib.write_gds(str(MACRO_LIB / "gds/open3dstack_padframe.gds"))

    wrapper_lib = gdstk.Library(unit=source.unit, precision=source.precision)
    wrapper_only = wrapper_lib.new_cell("open3dstack_user_project_wrapper")
    add_outline(wrapper_only, 0.0, 0.0, USER_W, USER_H, 20.0, 152, 5)
    wrapper_lib.write_gds(str(MACRO_LIB / "gds/open3dstack_user_project_wrapper_empty.gds"))


def lef_header() -> str:
    return """VERSION 5.8 ;
BUSBITCHARS "[]" ;
DIVIDERCHAR "/" ;
UNITS
  DATABASE MICRONS 1000 ;
END UNITS
"""


def lef_pin(name: str, rect: tuple[float, float, float, float], layer: str = PIN_LAYER) -> str:
    x0, y0, x1, y1 = rect
    return f"""  PIN {name}
    DIRECTION INOUT ;
    USE SIGNAL ;
    PORT
      LAYER {layer} ;
        RECT {fmt(x0)} {fmt(y0)} {fmt(x1)} {fmt(y1)} ;
    END
  END {name}
"""


def write_lefs(pads: list[Pad]) -> None:
    wl_pad_lef = lef_header() + f"""MACRO wl_pad
  CLASS PAD ;
  ORIGIN 0 0 ;
  FOREIGN wl_pad 0 0 ;
  SIZE {fmt(PAD_W)} BY {fmt(PAD_H)} ;
  SYMMETRY X Y ;
{lef_pin("PAD", (0.0, 0.0, PAD_W, PAD_H))}  OBS
    LAYER {PIN_LAYER} ;
      RECT 0 0 {fmt(PAD_W)} {fmt(PAD_H)} ;
  END
END wl_pad
END LIBRARY
"""
    (MACRO_LIB / "lef/wl_pad.lef").write_text(wl_pad_lef)

    frame = lef_header() + f"""MACRO open3dstack_padframe
  CLASS BLOCK ;
  ORIGIN 0 0 ;
  FOREIGN open3dstack_padframe 0 0 ;
  SIZE {fmt(DIE_W)} BY {fmt(DIE_H)} ;
  SYMMETRY X Y ;
"""
    for pad in pads:
        frame += lef_pin(pad.name, pad.bbox)
    frame += f"""  OBS
    LAYER {PIN_LAYER} ;
      RECT 0 0 {fmt(DIE_W)} {fmt(USER_Y0)} ;
      RECT 0 {fmt(USER_Y0 + USER_H)} {fmt(DIE_W)} {fmt(DIE_H)} ;
      RECT 0 0 {fmt(USER_X0)} {fmt(DIE_H)} ;
      RECT {fmt(USER_X0 + USER_W)} 0 {fmt(DIE_W)} {fmt(DIE_H)} ;
  END
END open3dstack_padframe
END LIBRARY
"""
    (MACRO_LIB / "lef/open3dstack_padframe.lef").write_text(frame)

    wrapper = lef_header() + f"""MACRO open3dstack_user_project_wrapper
  CLASS BLOCK ;
  ORIGIN 0 0 ;
  FOREIGN open3dstack_user_project_wrapper 0 0 ;
  SIZE {fmt(USER_W)} BY {fmt(USER_H)} ;
  SYMMETRY X Y ;
"""
    for pad in pads:
        wrapper += lef_pin(pad.name, pad.user_pin_bbox)
    wrapper += "END open3dstack_user_project_wrapper\nEND LIBRARY\n"
    (MACRO_LIB / "lef/open3dstack_user_project_wrapper_empty.lef").write_text(wrapper)


def write_pad_constraints(pads: list[Pad]) -> None:
    constraints_dir = ROOT / "open3dstack/constraints"
    constraints_dir.mkdir(parents=True, exist_ok=True)

    with (constraints_dir / "open3dstack_pads.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "index",
                "name",
                "side",
                "default_kind",
                "frame_center_x_um",
                "frame_center_y_um",
                "frame_bbox_um",
                "orientation",
                "user_wrapper_pin_bbox_um",
            ]
        )
        for pad in pads:
            writer.writerow(
                [
                    pad.index,
                    pad.name,
                    pad.side,
                    pad.default_kind,
                    fmt(pad.center_x),
                    fmt(pad.center_y),
                    " ".join(fmt(v) for v in pad.bbox),
                    f"R{pad.rotation_deg}",
                    " ".join(fmt(v) for v in pad.user_pin_bbox),
                ]
            )

    side_order = {side: [p.name for p in pads if p.side == side] for side in ["N", "S", "E", "W"]}
    pin_order = ""
    for side in ["N", "S", "E", "W"]:
        pin_order += f"#{side}\n" + "\n".join(side_order[side]) + "\n\n"
    (constraints_dir / "open3dstack_user_project_wrapper.pin_order.cfg").write_text(pin_order)

    tcl = f"""# Open3DStack padframe geometry and integration constraints.
set ::env(OPEN3DSTACK_DIE_AREA) "0 0 {fmt(DIE_W)} {fmt(DIE_H)}"
set ::env(OPEN3DSTACK_USER_AREA) "{fmt(USER_X0)} {fmt(USER_Y0)} {fmt(USER_X0 + USER_W)} {fmt(USER_Y0 + USER_H)}"
set ::env(OPEN3DSTACK_USER_WRAPPER_DIE_AREA) "0 0 {fmt(USER_W)} {fmt(USER_H)}"
set ::env(OPEN3DSTACK_PAD_COUNT) {len(pads)}
set ::env(OPEN3DSTACK_PAD_PITCH_UM) {fmt(PAD_PITCH)}
set ::env(OPEN3DSTACK_PAD_DEFAULT_KIND) analog
set ::env(OPEN3DSTACK_PAD_MAP) "$::env(DESIGN_DIR)/../../open3dstack/constraints/open3dstack_pads.csv"
set ::env(OPEN3DSTACK_PIN_ORDER_CFG) "$::env(DESIGN_DIR)/../../open3dstack/constraints/open3dstack_user_project_wrapper.pin_order.cfg"
"""
    (constraints_dir / "open3dstack_pad_constraints.tcl").write_text(tcl)

    openlane_dir = ROOT / "openlane/open3dstack_user_project_wrapper"
    openlane_dir.mkdir(parents=True, exist_ok=True)
    (openlane_dir / "pin_order.cfg").write_text(pin_order)


def port_lines(pads: list[Pad]) -> str:
    return ",\n".join(f"    inout wire {pad.name}" for pad in pads)


def bare_port_list(pads: list[Pad]) -> str:
    return " ".join(pad.name for pad in pads)


def write_verilog_and_flow(pads: list[Pad]) -> None:
    verilog_dir = ROOT / "open3dstack/verilog"
    verilog_dir.mkdir(parents=True, exist_ok=True)

    defines = """`ifndef OPEN3DSTACK_USER_DEFINES_V
`define OPEN3DSTACK_USER_DEFINES_V

`define OPEN3DSTACK_PAD_MODE_ANALOG  1'b0
`define OPEN3DSTACK_PAD_MODE_DIGITAL 1'b1

"""
    for pad in pads:
        defines += f"`ifndef OPEN3DSTACK_{pad.name}_MODE\n"
        defines += f"`define OPEN3DSTACK_{pad.name}_MODE `OPEN3DSTACK_PAD_MODE_ANALOG\n"
        defines += "`endif\n"
    defines += "\n`endif\n"
    (verilog_dir / "open3dstack_user_defines.v").write_text(defines)

    wrapper = f"""module open3dstack_user_project_wrapper (
{port_lines(pads)}
);
    // Empty analog-passive wrapper. Replace with the user's design.
endmodule
"""
    src_dir = ROOT / "openlane/open3dstack_user_project_wrapper/src"
    src_dir.mkdir(parents=True, exist_ok=True)
    (src_dir / "open3dstack_user_project_wrapper.v").write_text(wrapper)

    includes_dir = verilog_dir / "includes"
    includes_dir.mkdir(parents=True, exist_ok=True)
    includes = """-v ../../open3dstack/verilog/open3dstack_user_defines.v
-v ../../openlane/open3dstack_user_project_wrapper/src/open3dstack_user_project_wrapper.v
"""
    (includes_dir / "includes.rtl.open3dstack_user_project").write_text(includes)

    blackboxes = """// Open3DStack pad-only frame black boxes.
`ifndef OPEN3DSTACK_FRAME_BLACKBOXES_V
`define OPEN3DSTACK_FRAME_BLACKBOXES_V

(* blackbox *)
"""
    blackboxes += f"""module wl_pad (
    inout wire PAD
);
endmodule

(* blackbox *)
module open3dstack_padframe (
{port_lines(pads)}
);
endmodule

`endif
"""
    (MACRO_LIB / "verilog/open3dstack_frame_blackboxes.v").write_text(blackboxes)

    config = f"""# OpenLane template for an Open3DStack user project wrapper.
set design_dir $::env(DESIGN_DIR)
set macro_lib "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/tft3d_macros"

set ::env(DESIGN_NAME) open3dstack_user_project_wrapper
set ::env(DESIGN_IS_CORE) 0

set ::env(VERILOG_FILES) [list \\
    "$design_dir/../../open3dstack/verilog/open3dstack_user_defines.v" \\
    "$design_dir/src/open3dstack_user_project_wrapper.v" \\
]
set ::env(VERILOG_FILES_BLACKBOX) [list \\
    "$macro_lib/verilog/open3dstack_frame_blackboxes.v" \\
]
set ::env(EXTRA_LEFS) [list \\
    "$macro_lib/lef/open3dstack_padframe.lef" \\
    "$macro_lib/lef/wl_pad.lef" \\
]
set ::env(EXTRA_GDS_FILES) [list \\
    "$macro_lib/gds/open3dstack_padframe.gds" \\
    "$macro_lib/gds/wl_pad.gds" \\
]

set ::env(CLOCK_PORT) ""
set ::env(CLOCK_PERIOD) 10
set ::env(RUN_CTS) 0

set ::env(FP_SIZING) absolute
set ::env(DIE_AREA) "0 0 {fmt(USER_W)} {fmt(USER_H)}"
set ::env(CORE_AREA) "100 100 {fmt(USER_W - 100)} {fmt(USER_H - 100)}"
set ::env(FP_PIN_ORDER_CFG) "$design_dir/pin_order.cfg"
set ::env(PL_TARGET_DENSITY) 0.05

set ::env(FP_PDN_ENABLE_RAILS) 0
set ::env(FP_PDN_ENABLE_MACROS_GRID) 0
set ::env(RUN_LVS) 0
set ::env(RUN_CVC) 0
set ::env(RUN_MAGIC) 0
set ::env(RUN_MAGIC_DRC) 0
set ::env(RUN_KLAYOUT_DRC) 0
set ::env(RUN_KLAYOUT_XOR) 0
"""
    (ROOT / "openlane/open3dstack_user_project_wrapper/config.tcl").write_text(config)


def write_lib_and_spice(pads: list[Pad]) -> None:
    pins = "\n".join(f"    pin ({pad.name}) {{ direction : inout; }}" for pad in pads)
    lib = f"""library (open3dstack_frame_placeholders) {{
  delay_model : table_lookup;
  time_unit : "1ns";
  voltage_unit : "1V";
  current_unit : "1mA";
  pulling_resistance_unit : "1kohm";
  leakage_power_unit : "1nW";
  capacitive_load_unit (1,pf);

  cell (wl_pad) {{
    dont_touch : true;
    area : {fmt(PAD_W * PAD_H)};
    pin (PAD) {{ direction : inout; }}
  }}

  cell (open3dstack_padframe) {{
    dont_touch : true;
    area : {fmt(DIE_W * DIE_H)};
{pins}
  }}

  cell (open3dstack_user_project_wrapper) {{
    dont_touch : true;
    area : {fmt(USER_W * USER_H)};
{pins}
  }}
}}
"""
    (MACRO_LIB / "lib/open3dstack_frame_placeholders.lib").write_text(lib)

    portlist = bare_port_list(pads)
    spice = f"""* Open3DStack pad-only frame placeholders.

.subckt wl_pad PAD
.ends wl_pad

.subckt open3dstack_padframe {portlist}
.ends open3dstack_padframe

.subckt open3dstack_user_project_wrapper {portlist}
.ends open3dstack_user_project_wrapper
"""
    (MACRO_LIB / "spice/open3dstack_frame.spice").write_text(spice)


def write_readme(pads: list[Pad]) -> None:
    text = f"""# Open3DStack Pad-Only Frame

This package provides a Caravel-style pad-only frame for 3D_TFT integration.
It intentionally excludes management SoC/RISC-V content and only places
`wl_pad` pads around an empty user-design area.

## Geometry

| Item | Value |
| --- | --- |
| Die size | {fmt(DIE_W)} um x {fmt(DIE_H)} um |
| User wrapper area | {fmt(USER_W)} um x {fmt(USER_H)} um |
| User wrapper origin in frame | ({fmt(USER_X0)} um, {fmt(USER_Y0)} um) |
| Pad primitive | `wl_pad`, {fmt(PAD_W)} um x {fmt(PAD_H)} um |
| Pad pitch | {fmt(PAD_PITCH)} um |
| Total pads | {len(pads)} |

## Files

| File | Purpose |
| --- | --- |
| `pdk/tft3d_platform/libs.ref/tft3d_macros/gds/open3dstack_padframe.gds` | Physical pad-only frame GDS |
| `pdk/tft3d_platform/libs.ref/tft3d_macros/lef/open3dstack_padframe.lef` | Frame abstract with pad pins |
| `pdk/tft3d_platform/libs.ref/tft3d_macros/gds/open3dstack_user_project_wrapper_empty.gds` | Empty user-area placeholder |
| `pdk/tft3d_platform/libs.ref/tft3d_macros/lef/open3dstack_user_project_wrapper_empty.lef` | User wrapper abstract and pin locations |
| `pdk/tft3d_platform/libs.ref/tft3d_macros/verilog/open3dstack_frame_blackboxes.v` | Black-box views for frame macros |
| `pdk/tft3d_platform/libs.ref/tft3d_macros/lib/open3dstack_frame_placeholders.lib` | Placeholder Liberty for frame macros |
| `pdk/tft3d_platform/libs.ref/tft3d_macros/spice/open3dstack_frame.spice` | Placeholder SPICE for frame macros |
| `open3dstack/constraints/open3dstack_pads.csv` | Pad placement and default mode map |
| `open3dstack/constraints/open3dstack_user_project_wrapper.pin_order.cfg` | OpenLane pin order for user wrapper integration |
| `open3dstack/verilog/open3dstack_user_defines.v` | Per-pad analog/digital mode defaults |
| `openlane/open3dstack_user_project_wrapper/` | Empty OpenLane wrapper template |

## Pad Modes

All pads default to simple analog mode. To make a pad digital later, update the
pad map and override that pad's macro in `open3dstack_user_defines.v` from
`OPEN3DSTACK_PAD_MODE_ANALOG` to `OPEN3DSTACK_PAD_MODE_DIGITAL`, then add the
corresponding digital pad/buffer implementation.
"""
    out = ROOT / "open3dstack/README.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)


def main() -> None:
    pads = make_pads()
    for path in [
        MACRO_LIB / "gds",
        MACRO_LIB / "lef",
        MACRO_LIB / "verilog",
        MACRO_LIB / "lib",
        MACRO_LIB / "spice",
        ROOT / "open3dstack/constraints",
        ROOT / "openlane/open3dstack_user_project_wrapper/src",
    ]:
        path.mkdir(parents=True, exist_ok=True)
    generate_gds(pads)
    write_lefs(pads)
    write_pad_constraints(pads)
    write_verilog_and_flow(pads)
    write_lib_and_spice(pads)
    write_readme(pads)
    print(f"Generated Open3DStack padframe with {len(pads)} pads")


if __name__ == "__main__":
    main()
