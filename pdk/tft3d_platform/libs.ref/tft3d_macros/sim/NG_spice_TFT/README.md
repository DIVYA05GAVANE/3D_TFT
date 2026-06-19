# Stock ngspice TFT simulation

The original `id_vds_tft_n1.sp` deck is HSPICE/Verilog-A oriented and expects:

- `/apps/PDK/NCSU/FreePDK/FreePDK45/1.4/ncsu_basekit/models/hspice/hspice_nom.include`
- `.hdl "tft_n1.va"`

Stock ngspice on the remote Ubuntu PC does not load that Verilog-A `.hdl` model directly, so the compatible deck is:

```sh
./run_ngspice_tft.sh
```

It runs `id_vds_tft_n1_ngspice.sp`, which includes `tft_n1_ngspice.inc`. The include implements the same simple model from `tft_n1.va` with a native ngspice behavioral current source and the `g_n1_tbl.tbl` conductance values embedded as a PWL table.

Outputs:

- `id_vds_tft_n1_ngspice.dat`: whitespace table with `v(vd)` and `id_tft`
- `id_vds_tft_n1_ngspice.raw`: ASCII ngspice raw data
- `id_vds_tft_n1_ngspice.log`: ngspice run log
- `id_vds_tft_n1_ngspice.png`: plotted Id-Vds curve
