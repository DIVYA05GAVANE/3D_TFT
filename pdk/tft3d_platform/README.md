# Neutral 3D_TFT Platform PDK Shim

This directory is a minimal OpenLane PDK wrapper for the 3D_TFT platform assets.
It uses neutral repository-local names and contains the routing technology,
standard-cell, Liberty, GDS, CDL, SPICE, Verilog, and KLayout map files needed
by the layout flow.

The reusable 3D_TFT hard-macro views are kept in
`libs.ref/tft3d_macros/`. These are the platform-layer LEF/GDS and placeholder
Liberty, SPICE, Verilog, and simulation views used by OpenLane, including the
six extracted Stack SRAM array flavour macros. The original source GDS/CIF/LEF
files, source layer maps, and import archives remain under
`openlane_import/source/` at the repository root for traceability.

## Basic Simulation Models

- `libs.tech/ngspice/tft3d_platform.spice`: self-contained primitive and
  standard-cell SPICE models for circuit bring-up.
- `libs.tech/ngspice/tft3d_platform_primitives.spice`: basic `nch` transistor
  and `resmod` resistor models.
- `libs.ref/tft3d_sc_t5/spice/tft3d_sc_t5.spice`: simulator-clean standard-cell
  subcircuits.
- `libs.ref/tft3d_sc_t5/verilog/tft3d_sc_t5.v`: Verilog functional models for
  digital simulation.
- `libs.ref/tft3d_macros/spice/3d_tft_macros.spice`: placeholder SPICE models
  for the imported hard macros.
- `libs.ref/tft3d_macros/sim/3d_tft_macro_functional.v`: functional Verilog
  models for simple macro-level simulation.
- `libs.tech/ngspice/examples/`: runnable DC, transient, AC/noise, corner,
  temperature, and Monte Carlo example decks.
- `libs.tech/openflow/simulation.yml`: neutral manifest mapping simulation
  classes to tools and decks.

The OpenLane PDK config publishes these paths through `SPICE_MODEL_FILES`,
`SPICE_PRIMITIVE_MODELS`, `STD_CELL_SPICE`, `SIMULATION_MANIFEST`,
`VERILOG_MODELS`, and `TFT3D_MACRO_*` variables for flows that consume platform
and simulator views.

It is suitable for OpenLane integration with the existing 3D_TFT hard-macro
package. It is not a foundry signoff PDK: Magic, netgen, Calibre, DRC, LVS,
extraction, and tapeout checks still need validated decks and pin-accurate macro
views.
