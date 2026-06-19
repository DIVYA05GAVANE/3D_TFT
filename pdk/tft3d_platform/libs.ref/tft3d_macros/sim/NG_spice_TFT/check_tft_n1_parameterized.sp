Parameterized TFT n1 wrapper check
* Verifies that tft_n1_ngspice.inc accepts w/l/m parameters and that the
* macro-style nfet_w*_l5 wrappers map d g s pins into the measured d s g model.

.include "tft_n1_ngspice.inc"

.param Vd=1
.param Vg=3

Vd_base d_base 0 dc={Vd}
Vg_base g_base 0 dc={Vg}
Xbase d_base 0 g_base tft_n1_ngspice w=8e-6 l=3e-6 m=1

Vd_6 d_6 0 dc={Vd}
Vg_6 g_6 0 dc={Vg}
X6 d_6 g_6 0 nfet_w6u_l5

Vd_20 d_20 0 dc={Vd}
Vg_20 g_20 0 dc={Vg}
X20 d_20 g_20 0 nfet_w20p825_l5

Vd_24 d_24 0 dc={Vd}
Vg_24 g_24 0 dc={Vg}
X24 d_24 g_24 0 nfet_w24u_l5

.op
.print op i(Vd_base) i(Vd_6) i(Vd_20) i(Vd_24)

.end
