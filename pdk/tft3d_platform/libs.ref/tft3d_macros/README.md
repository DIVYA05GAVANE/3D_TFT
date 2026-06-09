# 3D_TFT Hard-Macro Reference Views

This library contains the PDK-facing views for the imported 3D_TFT hard macros.
OpenLane consumes these files through `EXTRA_LEFS`, `EXTRA_GDS_FILES`,
`EXTRA_LIBS`, `EXTRA_SPICE_FILES`, and `VERILOG_FILES_BLACKBOX`.

## Contents

- `gds/`: platform-layer GDS files used for final GDS merge.
- `lef/`: platform-layer LEF abstracts used for placement and routing.
- `lib/`: placeholder Liberty views for OpenSTA/OpenLane loading.
- `spice/`: placeholder SPICE models for bring-up and simple checks.
- `verilog/`: black-box Verilog declarations for synthesis/elaboration.
- `sim/`: functional Verilog models for simple digital simulation.

## Cell Views

The physical GDS and LEF views are stored as one file per macro because layout
tools commonly merge individual cell layouts. The logical and electrical views
are stored as one library file per view type, with one entry per macro inside
the file. That is intentional and matches normal PDK/library organization.

| Cell | Layout views | Netlist/interface views | Notes |
| --- | --- | --- | --- |
| `nfet_W20p825_L5` | `gds/nfet_W20p825_L5.gds`, `lef/nfet_W20p825_L5.lef` | `.subckt` in `spice/3d_tft_macros.spice`, `cell` in `lib/3d_tft_placeholders.lib`, modules in `verilog/3d_tft_blackboxes.v` and `sim/3d_tft_macro_functional.v` | Primitive-style TFT macro. |
| `nfet_W24u_L5` | `gds/nfet_W24u_L5.gds`, `lef/nfet_W24u_L5.lef` | `.subckt` in `spice/3d_tft_macros.spice`, `cell` in `lib/3d_tft_placeholders.lib`, modules in `verilog/3d_tft_blackboxes.v` and `sim/3d_tft_macro_functional.v` | Primitive-style TFT macro. |
| `nfet_W6u_L5` | `gds/nfet_W6u_L5.gds`, `lef/nfet_W6u_L5.lef` | `.subckt` in `spice/3d_tft_macros.spice`, `cell` in `lib/3d_tft_placeholders.lib`, modules in `verilog/3d_tft_blackboxes.v` and `sim/3d_tft_macro_functional.v` | Primitive-style TFT macro. |
| `INV_X4PC_T5_nmos` | `gds/INV_X4PC_T5_nmos.gds`, `lef/INV_X4PC_T5_nmos.lef` | `.subckt` in `spice/3d_tft_macros.spice`, `cell` in `lib/3d_tft_placeholders.lib`, modules in `verilog/3d_tft_blackboxes.v` and `sim/3d_tft_macro_functional.v` | Built from lower-level TFT layout blocks in GDS; current SPICE is a placeholder. |
| `wl_inv` | `gds/wl_inv.gds`, `lef/wl_inv.lef` | `.subckt` in `spice/3d_tft_macros.spice`, `cell` in `lib/3d_tft_placeholders.lib`, modules in `verilog/3d_tft_blackboxes.v` and `sim/3d_tft_macro_functional.v` | Hierarchical word-line macro. |
| `wl_prebuffer` | `gds/wl_prebuffer.gds`, `lef/wl_prebuffer.lef` | `.subckt` in `spice/3d_tft_macros.spice`, `cell` in `lib/3d_tft_placeholders.lib`, modules in `verilog/3d_tft_blackboxes.v` and `sim/3d_tft_macro_functional.v` | Hierarchical word-line macro. |
| `wl_sel` | `gds/wl_sel.gds`, `lef/wl_sel.lef` | `.subckt` in `spice/3d_tft_macros.spice`, `cell` in `lib/3d_tft_placeholders.lib`, modules in `verilog/3d_tft_blackboxes.v` and `sim/3d_tft_macro_functional.v` | Hierarchical word-line macro. |
| `stack_sram_array_f0` | `gds/stack_sram_array_f0.gds`, `lef/stack_sram_array_f0.lef` | physical-only placeholder entries in `spice/3d_tft_macros.spice`, `lib/3d_tft_placeholders.lib`, `verilog/3d_tft_blackboxes.v`, and `sim/3d_tft_macro_functional.v` | Upper-left bottom array flavour extracted from `Stack_SRAM_260605_F.gds`. |
| `stack_sram_array_f1` | `gds/stack_sram_array_f1.gds`, `lef/stack_sram_array_f1.lef` | physical-only placeholder entries in `spice/3d_tft_macros.spice`, `lib/3d_tft_placeholders.lib`, `verilog/3d_tft_blackboxes.v`, and `sim/3d_tft_macro_functional.v` | Upper-middle bottom array flavour extracted from `Stack_SRAM_260605_F.gds`. |
| `stack_sram_array_f2` | `gds/stack_sram_array_f2.gds`, `lef/stack_sram_array_f2.lef` | physical-only placeholder entries in `spice/3d_tft_macros.spice`, `lib/3d_tft_placeholders.lib`, `verilog/3d_tft_blackboxes.v`, and `sim/3d_tft_macro_functional.v` | Upper-right bottom array flavour extracted from `Stack_SRAM_260605_F.gds`. |
| `stack_sram_array_f3` | `gds/stack_sram_array_f3.gds`, `lef/stack_sram_array_f3.lef` | physical-only placeholder entries in `spice/3d_tft_macros.spice`, `lib/3d_tft_placeholders.lib`, `verilog/3d_tft_blackboxes.v`, and `sim/3d_tft_macro_functional.v` | Lower-left bottom array flavour extracted from `Stack_SRAM_260605_F.gds`. |
| `stack_sram_array_f4` | `gds/stack_sram_array_f4.gds`, `lef/stack_sram_array_f4.lef` | physical-only placeholder entries in `spice/3d_tft_macros.spice`, `lib/3d_tft_placeholders.lib`, `verilog/3d_tft_blackboxes.v`, and `sim/3d_tft_macro_functional.v` | Lower-middle bottom array flavour extracted from `Stack_SRAM_260605_F.gds`. |
| `stack_sram_array_f5` | `gds/stack_sram_array_f5.gds`, `lef/stack_sram_array_f5.lef` | physical-only placeholder entries in `spice/3d_tft_macros.spice`, `lib/3d_tft_placeholders.lib`, `verilog/3d_tft_blackboxes.v`, and `sim/3d_tft_macro_functional.v` | Lower-right bottom array flavour extracted from `Stack_SRAM_260605_F.gds`. |

## Netlist Organization

Keep `spice/3d_tft_macros.spice` as the single macro SPICE/CDL-style library
unless a downstream LVS or simulation tool specifically requires per-cell files.
One combined file avoids include-order problems for hierarchical macros such as
`wl_prebuffer`, which instantiates `INV_X4PC_T5_nmos`.

If verified extracted netlists become available later, add them beside the
placeholder file instead of replacing provenance:

```text
spice/
  3d_tft_macros.spice          # current bring-up placeholder
  3d_tft_macros_extracted.spice # extracted/verified SPICE, when available
cdl/
  3d_tft_macros.cdl            # LVS CDL, when available
```

Only split into `spice/cells/<cell>.spice` if a tool needs it. If you do split,
keep a top-level `spice/3d_tft_macros.spice` wrapper that includes the cells in
dependency order so OpenLane and simulation configs still point to one stable
file.

The same rule applies to Liberty and Verilog:

- Keep Liberty as a library-level file, normally one file per PVT/corner, with
  multiple `cell (...)` blocks inside.
- Keep black-box Verilog and simple functional simulation models as library
  files with one module per macro.
- Add more Liberty files only when real timing corners exist, for example
  `lib/typ_1p50v_25c.lib`, `lib/fast_1p65v_55c.lib`, and
  `lib/slow_1p35v_m10c.lib`.

## Array-Level Layout

The six `stack_sram_array_f*` macros are extracted from the bottom six array
regions in `Stack_SRAM_260605_F.gds`. The source GDS is flattened into one
`MainSymbol` cell, so the array names are repository-local flavour names ordered
left-to-right, top-to-bottom across those six bottom regions.

The Stack SRAM source layer map is retained at
`openlane_import/source/tech/Stack_SRAM_260605_F.map.txt`. The extracted array
GDS files preserve these source layers:

```text
31 SRAM_BG
32 SRAM_CH
33 SRAM_SD
34 SRAM_L2_BG
35 SRAM_L2_CH
36 SRAM_Hole
37 SRAM_L2_SD
40 WL Number
```

Layer 40 contains drawn WL-number geometry. It is not GDS text and it does not
provide named electrical pins. The array LEFs are therefore physical-only macro
abstracts with full routing obstructions and no pins. Add real LEF pins,
SPICE/CDL ports, Liberty pins, and Verilog ports after the array pin map is
known or after pin-labeled extracted views are available.

The original imported ZIPs, source-layout GDS files, and source LEF files are
kept under `openlane_import/source/` at the repository root. Keep those source
views separate from this library so the flow always uses the remapped platform
views.
