# NG_spice_TFT

## Model

`tft_n1_ngspice.inc` is a stock-ngspice translation of the original measured
TFT model:

- Source Verilog-A: `../TFT HSPICE/tft_n1.va`
- Source conductance table: `../TFT HSPICE/g_n1_tbl.tbl`
- Base measured device called out by the Verilog-A comment: `W=8`, `L=3`

The parameterized subckt is:

```spice
.subckt tft_n1_ngspice d s g w=8e-6 l=3e-6 m=1
```

The default `w`, `l`, and `m` reproduce the original measured table behavior.
For other sizes, the current is scaled as:

```text
Id_scaled = Id_measured * m * (w/l) / (8um/3um)
```

Assumptions and limits:

- This is a first-order W/L scaling of one measured W=8, L=3 TFT.
- It does not model geometry-dependent threshold shift, contacts, access
  resistance, fringing, traps, short-channel behavior, or per-geometry fitting.
- Values outside the measured Vgs table range use ngspice PWL extrapolation.
- The base model keeps the original Verilog-A pin order `d s g`.
- Convenience wrappers `nfet_w6u_l5`, `nfet_w20p825_l5`, and `nfet_w24u_l5`
  use the macro pin order `d g s` and pass their `w`, `l`, and `m` parameters
  into `tft_n1_ngspice`.

Example macro-style instance:

```spice
.include "tft_n1_ngspice.inc"
Xpass bl sel array_bl nfet_w6u_l5
Xwide out gate src nfet_w24u_l5 m=2
```

Quick parameterization check:

```bash
ngspice -b -o check_tft_n1_parameterized.log check_tft_n1_parameterized.sp
```

## Run with ngspice

```bash
./run_ngspice_tft.sh
```

Direct command:

```bash
ngspice -b -o id_vds_tft_n1_ngspice.log id_vds_tft_n1_ngspice.sp
```

## Simulation results

Sweep: `Vd = -3 V` to `5 V`, step `0.01 V`, with `Vg = 3 V`.

Output files:

- `id_vds_tft_n1_ngspice.dat`
- `id_vds_tft_n1_ngspice.raw`
- `id_vds_tft_n1_ngspice.log`
- `id_vds_tft_n1_ngspice.png`

Selected data points from `id_vds_tft_n1_ngspice.dat`:

| Vd (V) | Id (A) |
|---:|---:|
| -3.0 | -5.424e-04 |
| 0.0 | -1.7865e-18 |
| 2.0 | 1.816e-04 |
| 5.0 | 4.540e-04 |
