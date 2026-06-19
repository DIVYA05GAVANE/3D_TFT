# 3D TFT Macro PDK Files

This repository is mainly a small PDK-facing package for the 3D TFT macro views in:

```text
pdk/tft3d_platform/libs.ref/tft3d_macros
```

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
