# NG-spice macro simulations

This directory contains stock-ngspice testbenches for the TFT macro netlists in `../../spice`.

The original extracted decks are HSPICE-oriented and use `NMOS_VTG` plus a missing FreePDK include. The local ngspice models here replace those cells with a parameterized behavioral TFT model built from the measured `g_n1_tbl.tbl` conductance table and scaled by `W/L` and `M`.

Run all decks:

```sh
./run_all.sh
```

Run a Monte Carlo sweep over the same ngspice decks:

```sh
python3 scripts/run_montecarlo.py --samples 64 --jobs 4
```

The Monte Carlo runner reuses the checked-in `models/` and `tb/` files and writes generated sample decks under `montecarlo/`. Its TFT variation model is intended as a stress model for this measured-table behavioral abstraction: it scales the base conductance table by `W/L` and `M`, applies global conductance/Vgs/W/L/internal-R/internal-C process terms, and applies local area-aware TFT mismatch terms per device instance. It is not a silicon-qualified statistical process model.

Outputs are regenerated in:

- `results/*.dat`: ASCII tables for plotting/checking
- `results/*.raw`: ASCII ngspice raw files
- `results/*.log`: ngspice logs
- `plots/*.svg`: generated plots
- `results/summary.csv`, `results/summary.json`, `results/REPORT.md`: pass/fail summary

Monte Carlo outputs are regenerated in:

- `montecarlo/results/summary.csv`, `aggregate.csv`, `variation_manifest.csv`, `failures.csv`, `REPORT.md`
- `montecarlo/plots/*_metric_hist.svg`
- `montecarlo/samples/s*/`: generated model/deck/result copies for each sample

Covered decks:

- `nfet_w6u_l5`, `nfet_w20p825_l5`, `nfet_w24u_l5` Id-Vds
- `nfet_w6u_l5` Id-Vg
- `inv_x4pc_t5_nmos`, `nand3_x4rl_t5`
- `wl_inv`, `wl_prebuffer`, `wl_sel`, `wl_driver_nmos`
- `row_decoder_3to8_nmos`, `column_decoder_3to8_nmos`
- `analog_mux_2to1_diff_nmos`, `analog_mux_2to1_diff_nmos_schematic`, `analog_mux_bl_sl_nmos`
- `precharge_equalizer_nmos_6u`
- `opamp_6u`
- `write_driver`
- `3d_tft_macros.spice` primitive/inverter/NAND/WL wrapper checks

Physical-only empty placeholders are listed as skipped in the report.
