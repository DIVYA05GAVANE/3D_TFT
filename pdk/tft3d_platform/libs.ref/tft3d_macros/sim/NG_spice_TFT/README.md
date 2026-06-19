# NG_spice_TFT

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
