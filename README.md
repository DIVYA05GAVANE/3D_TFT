# 3D_TFT OpenLane Package

This repository packages the 3D_TFT layout blocks, a neutral local OpenLane PDK
shim, and one OpenLane layout flow entrypoint.

The repo uses neutral local naming for the PDK, library, and flow assets.
The default flow uses:

```text
PDK_ROOT=$PWD/pdk
PDK=tft3d_platform
STD_CELL_LIBRARY=tft3d_sc_t5
DESIGN=openlane/tft3d_macro_layout
```

## Contents

- `pdk/tft3d_platform/`: local OpenLane-compatible platform PDK shim.
- `pdk/tft3d_platform/libs.ref/tft3d_macros/`: PDK-facing 3D_TFT hard-macro
  LEF, GDS, Liberty, SPICE, Verilog, and simulation views used by OpenLane,
  including the extracted Stack SRAM array flavour macros.
- `openlane/tft3d_macro_layout/`: OpenLane layout target using the available 3D_TFT hard macros.
- `openlane_import/source/`: original imported ZIPs, source-layout GDS files,
  CIF files, source LEF files, and source layer maps retained for provenance.
- `openlane_import/metadata/` and `openlane_import/reports/`: import audit
  metadata and reports for the 3D_TFT macro blocks.
- `openlane_import/tech/`: layer maps retained for interoperability.
- `scripts/run_openlane_flow.sh`: the single repo script for launching the OpenLane flow.

## Run OpenLane

From the repo root on the Ubuntu OpenLane machine:

```sh
./scripts/run_openlane_flow.sh
```

Optional overrides:

```sh
OPENLANE_ROOT=$HOME/OpenLane \
OPENLANE_DESIGN_DIR=openlane/tft3d_macro_layout \
OPENLANE_TAG=layout \
./scripts/run_openlane_flow.sh
```

The runner validates the required PDK, LEF, GDS, Liberty, and black-box Verilog
inputs before invoking OpenLane. It works inside an OpenLane container or through
the local `$OPENLANE_ROOT` Docker wrapper path.

## Basic Simulation Models

The local PDK includes simulator-facing model files for OpenFlow/OpenLane-style
automation and standalone circuit bring-up:

- `pdk/tft3d_platform/libs.tech/ngspice/tft3d_platform.spice`: self-contained
  primitive plus standard-cell SPICE model file.
- `pdk/tft3d_platform/libs.tech/ngspice/tft3d_platform_primitives.spice`: basic
  `nch` and `resmod` primitive models.
- `pdk/tft3d_platform/libs.ref/tft3d_sc_t5/spice/tft3d_sc_t5.spice`:
  simulator-clean standard-cell subcircuits.
- `pdk/tft3d_platform/libs.ref/tft3d_sc_t5/verilog/tft3d_sc_t5.v`: Verilog
  functional models for digital simulation.
- `pdk/tft3d_platform/libs.ref/tft3d_macros/spice/3d_tft_macros.spice`: basic
  SPICE placeholders for the imported 3D_TFT hard macros.
- `pdk/tft3d_platform/libs.tech/openflow/simulation.yml`: neutral simulation
  manifest for flow automation.

Tool mapping:

- `ngspice`: DC transfer, DC output, transient switching, AC/noise,
  corner-style, temperature-style, and Monte Carlo-style SPICE decks.
- `iverilog`: digital functional simulation of the OpenLane macro layout
  wrapper using functional macro models.
- `verilator`: available on the remote for Verilog lint/compile workflows.

The SPICE example decks live in
`pdk/tft3d_platform/libs.tech/ngspice/examples/` and are intended to be run from
the repository root so relative includes resolve correctly.

## Signoff Boundary

The available macro GDS files do not contain named pin labels. The current LEF,
Liberty, Verilog, and SPICE macro views are integration placeholders so OpenLane
can place, route, stream a merged layout, and support basic circuit bring-up.
Before signoff, replace those views with pin-accurate and process-validated
macro views plus validated DRC/LVS/PEX decks.
