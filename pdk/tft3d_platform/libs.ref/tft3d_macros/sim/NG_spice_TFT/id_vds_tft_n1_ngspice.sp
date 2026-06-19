TFT n1 W=8 L=3 Id-Vds sweep - stock ngspice deck
* This is the ngspice-compatible version of id_vds_tft_n1.sp.
* The original deck uses an HSPICE-only PDK include and Verilog-A .hdl.
* This deck uses tft_n1_ngspice.inc, a native ngspice behavioral model.

.include "tft_n1_ngspice.inc"

.param Vg=3
.param Wtft=8e-6
.param Ltft=3e-6
.param Mtft=1
.temp 27.0

Vss vs 0 dc=0
Vdsrc vd 0 dc=0
Vgsrc vg 0 dc={Vg}
Xn1 vd vs vg tft_n1_ngspice w={Wtft} l={Ltft} m={Mtft}

.dc Vdsrc -3.0 5.0 10e-3
.print dc v(vd) i(Vdsrc)

.control
run
set filetype=ascii
set wr_singlescale
set wr_vecnames
let id_tft = -i(vdsrc)
wrdata id_vds_tft_n1_ngspice.dat v(vd) id_tft
write id_vds_tft_n1_ngspice.raw
.endc

.end
