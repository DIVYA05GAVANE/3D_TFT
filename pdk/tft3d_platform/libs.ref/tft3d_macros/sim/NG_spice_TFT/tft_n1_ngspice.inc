* tft_n1 native ngspice model for stock ngspice builds.
*
* Base model:
* - Derived from ../TFT HSPICE/tft_n1.va and ../TFT HSPICE/g_n1_tbl.tbl.
* - The Verilog-A comment identifies the measured base device as TFT W=8, L=3.
* - The table is channel conductance gch versus the effective Vgs chosen by
*   the original source/drain orientation rule.
*
* Parameterization assumptions:
* - w and l are electrical scale factors around the measured W=8um, L=3um
*   base device; defaults preserve the original measured curve.
* - Current is scaled linearly by m*(w/l)/(8um/3um). This is a first-order
*   sheet-conductance assumption and does not model geometry-dependent
*   threshold, contacts, access resistance, fringing, traps, or short-channel
*   effects.
* - Extrapolation outside the measured Vgs table range is ngspice PWL
*   extrapolation, not additional measurement data.
* - Pin order is d s g to match the original Verilog-A module and Id-Vds deck.
.subckt tft_n1_ngspice d s g w=8e-6 l=3e-6 m=1
Bch d s I={m*(w/8e-6)*(3e-6/l)*V(d,s)*pwl(((V(s)<V(d)) ? V(g,s) : V(g,d)),
+ -3, 1.84e-13,
+ -2.95, 2.69e-12,
+ -2.9, 6.9e-13,
+ -2.85, 3.48e-12,
+ -2.8, 2.73e-12,
+ -2.75, 2.82e-12,
+ -2.7, 1.69e-12,
+ -2.65, 4.23e-12,
+ -2.6, 1.8e-12,
+ -2.55, 3.01e-12,
+ -2.5, 2.02e-12,
+ -2.45, 2.2e-12,
+ -2.4, 3.82e-12,
+ -2.35, 5.98e-12,
+ -2.3, 3.38e-12,
+ -2.25, 4.28e-12,
+ -2.2, 5.29e-12,
+ -2.15, 6.23e-12,
+ -2.1, 5.21e-12,
+ -2.05, 4.19e-12,
+ -2, 4.52e-12,
+ -1.95, 5.62e-12,
+ -1.9, 5.73e-12,
+ -1.85, 4.21e-12,
+ -1.8, 4.85e-12,
+ -1.75, 5.47e-12,
+ -1.7, 4.55e-12,
+ -1.65, 4.68e-12,
+ -1.6, 6.33e-12,
+ -1.55, 5.23e-12,
+ -1.5, 7.2e-12,
+ -1.45, 8.31e-12,
+ -1.4, 6.14e-12,
+ -1.35, 7.9e-12,
+ -1.3, 6.65e-12,
+ -1.25, 6.03e-12,
+ -1.2, 3.81e-12,
+ -1.15, 2.77e-12,
+ -1.1, 9.44e-12,
+ -1.05, 2.36e-11,
+ -1, 4.84e-11,
+ -0.95, 8.89e-11,
+ -0.9, 1.72e-10,
+ -0.85, 3.13e-10,
+ -0.8, 5.71e-10,
+ -0.75, 1.03e-09,
+ -0.7, 1.85e-09,
+ -0.65, 3.27e-09,
+ -0.6, 5.72e-09,
+ -0.55, 1.05e-08,
+ -0.5, 1.75e-08,
+ -0.45, 2.82e-08,
+ -0.4, 4.44e-08,
+ -0.35, 5.76e-08,
+ -0.3, 9.44e-08,
+ -0.25, 1.44e-07,
+ -0.2, 2.1e-07,
+ -0.15, 2.98e-07,
+ -0.1, 4.12e-07,
+ -0.05, 5.12e-07,
+ 0, 7.01e-07,
+ 0.05, 9.27e-07,
+ 0.1, 1.2e-06,
+ 0.15, 1.52e-06,
+ 0.2, 1.9e-06,
+ 0.25, 2.33e-06,
+ 0.3, 2.83e-06,
+ 0.35, 3.39e-06,
+ 0.4, 4.02e-06,
+ 0.45, 4.72e-06,
+ 0.5, 5.32e-06,
+ 0.55, 6.2e-06,
+ 0.6, 7.14e-06,
+ 0.65, 8.15e-06,
+ 0.7, 9.23e-06,
+ 0.75, 1.04e-05,
+ 0.8, 1.16e-05,
+ 0.85, 1.29e-05,
+ 0.9, 1.43e-05,
+ 0.95, 1.57e-05,
+ 1, 1.72e-05,
+ 1.05, 1.87e-05,
+ 1.1, 2.03e-05,
+ 1.15, 2.2e-05,
+ 1.2, 2.37e-05,
+ 1.25, 2.54e-05,
+ 1.3, 2.72e-05,
+ 1.35, 2.9e-05,
+ 1.4, 3.09e-05,
+ 1.45, 3.28e-05,
+ 1.5, 3.47e-05,
+ 1.55, 3.66e-05,
+ 1.6, 3.86e-05,
+ 1.65, 4.06e-05,
+ 1.7, 4.26e-05,
+ 1.75, 4.46e-05,
+ 1.8, 4.66e-05,
+ 1.85, 4.86e-05,
+ 1.9, 4.99e-05,
+ 1.95, 5.21e-05,
+ 2, 5.42e-05,
+ 2.05, 5.62e-05,
+ 2.1, 5.83e-05,
+ 2.15, 6.03e-05,
+ 2.2, 6.23e-05,
+ 2.25, 6.43e-05,
+ 2.3, 6.63e-05,
+ 2.35, 6.83e-05,
+ 2.4, 7.02e-05,
+ 2.45, 7.21e-05,
+ 2.5, 7.39e-05,
+ 2.55, 7.58e-05,
+ 2.6, 7.76e-05,
+ 2.65, 7.94e-05,
+ 2.7, 8.11e-05,
+ 2.75, 8.29e-05,
+ 2.8, 8.45e-05,
+ 2.85, 8.62e-05,
+ 2.9, 8.78e-05,
+ 2.95, 8.93e-05,
+ 3, 9.08e-05)}
.ends tft_n1_ngspice

* Three-terminal macro wrappers for extracted TFT macro netlists.
* These use the macro pin order d g s, then call the measured model's d s g
* order internally. The body terminal used by older NMOS placeholders is not
* part of the measured table model.
.subckt nfet_w6u_l5 d g s l=5e-6 w=6e-6 m=1
X0 d s g tft_n1_ngspice w={w} l={l} m={m}
.ends nfet_w6u_l5

.subckt nfet_w20p825_l5 d g s l=5e-6 w=20.825e-6 m=1
X0 d s g tft_n1_ngspice w={w} l={l} m={m}
.ends nfet_w20p825_l5

.subckt nfet_w24u_l5 d g s l=5e-6 w=24e-6 m=1
X0 d s g tft_n1_ngspice w={w} l={l} m={m}
.ends nfet_w24u_l5
