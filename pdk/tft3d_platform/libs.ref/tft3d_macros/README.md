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
| `wl_pad` | `gds/wl_pad.gds`, `lef/wl_pad.lef` | `module` in `verilog/open3dstack_frame_blackboxes.v`, `.subckt` in `spice/open3dstack_frame.spice`, `cell` in `lib/open3dstack_frame_placeholders.lib` | Standalone WL-end pad primitive used by the Open3DStack frame. |
| `open3dstack_padframe` | `gds/open3dstack_padframe.gds`, `lef/open3dstack_padframe.lef` | `module` in `verilog/open3dstack_frame_blackboxes.v`, `.subckt` in `spice/open3dstack_frame.spice`, `cell` in `lib/open3dstack_frame_placeholders.lib` | 25,000um x 15,000um pad-only frame using `wl_pad` around all four sides. |
| `open3dstack_user_project_wrapper` | `gds/open3dstack_user_project_wrapper_empty.gds`, `lef/open3dstack_user_project_wrapper_empty.lef` | Empty user wrapper template under `openlane/open3dstack_user_project_wrapper/` | 23,000um x 13,000um user-design area for integration inside the frame. |
| `stack_sram_array_f0` | `gds/stack_sram_array_f0.gds`, `lef/stack_sram_array_f0.lef` | physical-only placeholder entries in `spice/3d_tft_macros.spice`, `lib/3d_tft_placeholders.lib`, `verilog/3d_tft_blackboxes.v`, and `sim/3d_tft_macro_functional.v` | Upper-left bottom array flavour extracted from `Stack_SRAM_260605_F.gds`. |
| `stack_sram_array_f1` | `gds/stack_sram_array_f1.gds`, `lef/stack_sram_array_f1.lef` | physical-only placeholder entries in `spice/3d_tft_macros.spice`, `lib/3d_tft_placeholders.lib`, `verilog/3d_tft_blackboxes.v`, and `sim/3d_tft_macro_functional.v` | Upper-middle bottom array flavour extracted from `Stack_SRAM_260605_F.gds`. |
| `stack_sram_array_f2` | `gds/stack_sram_array_f2.gds`, `lef/stack_sram_array_f2.lef` | physical-only placeholder entries in `spice/3d_tft_macros.spice`, `lib/3d_tft_placeholders.lib`, `verilog/3d_tft_blackboxes.v`, and `sim/3d_tft_macro_functional.v` | Upper-right bottom array flavour extracted from `Stack_SRAM_260605_F.gds`. |
| `stack_sram_array_f3` | `gds/stack_sram_array_f3.gds`, `lef/stack_sram_array_f3.lef` | physical-only placeholder entries in `spice/3d_tft_macros.spice`, `lib/3d_tft_placeholders.lib`, `verilog/3d_tft_blackboxes.v`, and `sim/3d_tft_macro_functional.v` | Lower-left bottom array flavour extracted from `Stack_SRAM_260605_F.gds`. |
| `stack_sram_array_f4` | `gds/stack_sram_array_f4.gds`, `lef/stack_sram_array_f4.lef` | physical-only placeholder entries in `spice/3d_tft_macros.spice`, `lib/3d_tft_placeholders.lib`, `verilog/3d_tft_blackboxes.v`, and `sim/3d_tft_macro_functional.v` | Lower-middle bottom array flavour extracted from `Stack_SRAM_260605_F.gds`. |
| `stack_sram_array_f5` | `gds/stack_sram_array_f5.gds`, `lef/stack_sram_array_f5.lef` | physical-only placeholder entries in `spice/3d_tft_macros.spice`, `lib/3d_tft_placeholders.lib`, `verilog/3d_tft_blackboxes.v`, and `sim/3d_tft_macro_functional.v` | Lower-right bottom array flavour extracted from `Stack_SRAM_260605_F.gds`. |

## GDS Layer Mapping

The following stack map applies to every `stack_sram_array_f*` GDS file, ordered
from layer 1 to layer 2:

| Stack level | Source layer | Final GDS layer/datatype | Meaning |
| --- | --- | --- | --- |
| Layer 1 FEFET | `L31` | `31/0` | FEFET gate, metal -2 |
| Layer 1 FEFET | `L32` | `32/0` | FEFET channel |
| Layer 1 FEFET | `L33` | `33/0` | FEFET source/drain, metal -1 |
| Layer 1 FEFET | `L36` | `36/0` | FEFET M-1/M-2 via connect |
| Layer 2 upper TFT | `L35` | `3/0` | Upper channel active area |
| Layer 2 upper TFT | `L34` | `8/0` | Upper gate and M1 conductor |
| Layer 2 upper TFT | `L36` | `9/0` | Upper M1-M2 via open/connect |
| Layer 2 upper TFT | `L37` | `10/0` | Upper M2 source/drain conductor |
| Annotation | `L40` | `40/0` | Drawn WL-number geometry |

For stack SRAM arrays, `L36` appears in both layer contexts: layer 1 `L36`
remains `36/0`, while layer 2 upper TFT `L36` maps to `9/0`.

The common layer-2 TFT mask numbers are:

| GDS layer/datatype | Meaning |
| --- | --- |
| `3/0` | Channel active area |
| `8/0` | Gate and M1 conductor |
| `9/0` | M1-M2 via open/connect |
| `10/0` | M2 source/drain conductor |

Imported or older aliases in the TFT primitive, inverter, and word-line macro
GDS files are normalized into those layers:

| Source/old layer | Normalized layer |
| --- | --- |
| `4/0`, `8/0`, `8/2`, `11/0`, `20/0` | `8/0` gate and M1 conductor |
| `7/0`, `9/0`, `30/0`, `41/0` | `9/0` M1-M2 via open/connect |
| `10/0`, `10/2`, `21/0` | `10/0` M2 source/drain conductor |
| `3/0` | `3/0` channel active area |
