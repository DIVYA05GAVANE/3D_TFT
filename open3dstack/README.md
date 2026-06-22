# Open3DStack Pad-Only Frame

This package provides a Caravel-style pad-only frame for 3D_TFT integration.
It intentionally excludes management SoC/RISC-V content and only places
`wl_pad` pads around an empty user-design area.

## Geometry

| Item | Value |
| --- | --- |
| Die size | 25000 um x 22000 um |
| User wrapper area | 23000 um x 20000 um |
| User wrapper origin in frame | (1000 um, 1000 um) |
| Pad primitive | `wl_pad`, 100 um x 130 um |
| Pad pitch | 500 um |
| Total pads | 184 |

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
