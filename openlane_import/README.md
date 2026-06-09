# 3D_TFT Import Sources

This folder keeps the original imported 3D_TFT source material and audit data.
The OpenLane-ready, platform-layer hard-macro views live in the PDK reference
library at `../pdk/tft3d_platform/libs.ref/tft3d_macros/`.

## Contents

- `source/archives/`: original imported ZIP archives.
- `source/gds/`: extracted source-layout GDS files.
- `source/lef/`: source LEF abstracts using FreePDK45-style layer names.
- `metadata/cells.json`: size and placeholder-port metadata for the available cells.
- `reports/gds_audit.txt`: audited top cells, dimensions, layers, child refs, and label status.
- `tech/freepdk45.layermap`: retained source-layout layer map.
- `tech/freepdk45.def2gds.map`: OpenLane/KLayout DEF-to-GDS map for FreePDK45-numbered stream-out.
- `config.tcl.example`: snippet for importing the PDK-facing macro views into
  another OpenLane design.

## Limitation

The available GDS files do not contain named pin labels. The LEF pin shapes,
Verilog port lists, Liberty timing, and SPICE macro views are placeholders for
OpenLane integration and basic circuit bring-up only. Replace them with
authoritative pin-labeled and extracted views before signoff or LVS.
