# 3D TFT Macro PDK Files

This repository is mainly a small PDK-facing package for the 3D TFT macro views in:

```text
pdk/tft3d_platform/libs.ref/tft3d_macros
```

## First Tapeout Results

[VLSI 2026 paper draft: 3D-Stacked Cross-Coupled ZnO/Fe-ZnO TFT Differential Bit-Cell Enabling High-Density Memory and BCAM Hamming-Distance Comparison](docs/papers/VLSI2026_01_20_v5.pdf)

This first tapeout demonstrates a 3D-stacked differential TFT bit-cell that combines ZnO access TFTs with Fe-ZnO storage TFTs for compact memory operation and BCAM-style Hamming-distance comparison.

This process direction is useful because it targets an 8-inch, open-PDK-friendly 3D transistor platform rather than a closed custom flow. TFT access devices and ferroelectric FET/TFT storage devices can be stacked monolithically, so memory, search, and in-memory-compute primitives can be built above or alongside CMOS-style routing without consuming the same 2D footprint. Keeping the layouts, SPICE decks, GDS/LEF views, and ngspice testbenches in an open library format makes the process easier to reproduce, simulate, and extend with open-source tools.

<img src="docs/assets/e6_nanofab_nus.png" alt="E6 NanoFab at the National University of Singapore" width="360">

The work is associated with E6NanoFab at the National University of Singapore, a micro-nanofabrication research facility at Block E6 of the NUS Engineering campus. E6NanoFab supports academic and industrial work in nanotechnology and microelectronics, with cleanroom and dry/wet lab infrastructure for frontend, backend-of-line, and packaging-oriented process development. See the official [E6NanoFab overview](https://cde.nus.edu.sg/e6nanofab/) and [facility introduction](https://cde.nus.edu.sg/e6nanofab/about/).

## Community

Discuss this PDK in the BM Labs Matrix room: https://matrix.to/#/#BM_LABS:fossi-chat.org

## What This Folder Contains

`tft3d_macros` collects the files a layout or simulation flow needs for the 3D TFT macros:

- `gds/`: full layout GDS files for the imported hard macros and generated Open3DStack layouts.
- `lef/`: abstract layout views used by place-and-route tools.
- `lib/`: timing/library placeholder views.
- `spice/`: SPICE macro netlists and placeholder circuit views.
- `verilog/`: black-box Verilog views for digital integration.
- `sim/`: functional simulation views.
- `TFT HSPICE/`: the original single-TFT HSPICE/Verilog-A files.
- `NG_spice_TFT/`: a stock-ngspice version of the single-TFT Id-Vds simulation.

## Run The TFT ngspice Simulation

Install `ngspice`, then run:

```sh
cd pdk/tft3d_platform/libs.ref/tft3d_macros/NG_spice_TFT
./run_ngspice_tft.sh
```

The script runs:

```text
id_vds_tft_n1_ngspice.sp
```

That deck includes:

```text
tft_n1_ngspice.inc
```

The ngspice include implements the same simple TFT behavior as `TFT HSPICE/tft_n1.va` and uses the same conductance data from `TFT HSPICE/g_n1_tbl.tbl`, converted into a native ngspice PWL expression.

## Simulation Outputs

After running the script, check the generated files:

- `id_vds_tft_n1_ngspice.dat`: Id-Vds data table.
- `id_vds_tft_n1_ngspice.raw`: ASCII ngspice raw output.
- `id_vds_tft_n1_ngspice.log`: ngspice run log.

A reference plot is also included as `id_vds_tft_n1_ngspice.png`.

The original HSPICE/Verilog-A files are kept in `TFT HSPICE/` for reference, but `NG_spice_TFT/` is the easiest place to start with standard ngspice.
