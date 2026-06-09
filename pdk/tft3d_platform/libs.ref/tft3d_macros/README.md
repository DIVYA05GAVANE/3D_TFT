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

The original imported ZIPs, source-layout GDS files, and source LEF files are
kept under `openlane_import/source/` at the repository root. Keep those source
views separate from this library so the flow always uses the remapped platform
views.
