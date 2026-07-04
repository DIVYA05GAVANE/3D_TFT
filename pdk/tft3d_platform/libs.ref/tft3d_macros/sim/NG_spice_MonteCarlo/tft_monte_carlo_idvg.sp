TFT n1 Id-Vg Monte Carlo - stock ngspice
* FlexIC-style parallel sampled devices using agauss(...).

.include "../NG_spice_TFT/tft_n1_ngspice.inc"

.param Vd=0.1
.param Wnom=8e-6
.param Lnom=3e-6
.param Mnom=1
.param Vshift3s=0.30
.temp 27.0

Vgsrc g 0 PWL(0 -3 1u -3 7u 3 8u 3)

Vd00 d00 0 dc={Vd}
Vsh00 g g00 dc={agauss(0,Vshift3s,3)}
Xmc00 d00 0 g00 tft_n1_ngspice w={agauss(Wnom,0.40e-6,3)} l={agauss(Lnom,0.15e-6,3)} m={agauss(Mnom,0.08,3)}
Vd01 d01 0 dc={Vd}
Vsh01 g g01 dc={agauss(0,Vshift3s,3)}
Xmc01 d01 0 g01 tft_n1_ngspice w={agauss(Wnom,0.40e-6,3)} l={agauss(Lnom,0.15e-6,3)} m={agauss(Mnom,0.08,3)}
Vd02 d02 0 dc={Vd}
Vsh02 g g02 dc={agauss(0,Vshift3s,3)}
Xmc02 d02 0 g02 tft_n1_ngspice w={agauss(Wnom,0.40e-6,3)} l={agauss(Lnom,0.15e-6,3)} m={agauss(Mnom,0.08,3)}
Vd03 d03 0 dc={Vd}
Vsh03 g g03 dc={agauss(0,Vshift3s,3)}
Xmc03 d03 0 g03 tft_n1_ngspice w={agauss(Wnom,0.40e-6,3)} l={agauss(Lnom,0.15e-6,3)} m={agauss(Mnom,0.08,3)}
Vd04 d04 0 dc={Vd}
Vsh04 g g04 dc={agauss(0,Vshift3s,3)}
Xmc04 d04 0 g04 tft_n1_ngspice w={agauss(Wnom,0.40e-6,3)} l={agauss(Lnom,0.15e-6,3)} m={agauss(Mnom,0.08,3)}
Vd05 d05 0 dc={Vd}
Vsh05 g g05 dc={agauss(0,Vshift3s,3)}
Xmc05 d05 0 g05 tft_n1_ngspice w={agauss(Wnom,0.40e-6,3)} l={agauss(Lnom,0.15e-6,3)} m={agauss(Mnom,0.08,3)}
Vd06 d06 0 dc={Vd}
Vsh06 g g06 dc={agauss(0,Vshift3s,3)}
Xmc06 d06 0 g06 tft_n1_ngspice w={agauss(Wnom,0.40e-6,3)} l={agauss(Lnom,0.15e-6,3)} m={agauss(Mnom,0.08,3)}
Vd07 d07 0 dc={Vd}
Vsh07 g g07 dc={agauss(0,Vshift3s,3)}
Xmc07 d07 0 g07 tft_n1_ngspice w={agauss(Wnom,0.40e-6,3)} l={agauss(Lnom,0.15e-6,3)} m={agauss(Mnom,0.08,3)}
Vd08 d08 0 dc={Vd}
Vsh08 g g08 dc={agauss(0,Vshift3s,3)}
Xmc08 d08 0 g08 tft_n1_ngspice w={agauss(Wnom,0.40e-6,3)} l={agauss(Lnom,0.15e-6,3)} m={agauss(Mnom,0.08,3)}
Vd09 d09 0 dc={Vd}
Vsh09 g g09 dc={agauss(0,Vshift3s,3)}
Xmc09 d09 0 g09 tft_n1_ngspice w={agauss(Wnom,0.40e-6,3)} l={agauss(Lnom,0.15e-6,3)} m={agauss(Mnom,0.08,3)}
Vd10 d10 0 dc={Vd}
Vsh10 g g10 dc={agauss(0,Vshift3s,3)}
Xmc10 d10 0 g10 tft_n1_ngspice w={agauss(Wnom,0.40e-6,3)} l={agauss(Lnom,0.15e-6,3)} m={agauss(Mnom,0.08,3)}
Vd11 d11 0 dc={Vd}
Vsh11 g g11 dc={agauss(0,Vshift3s,3)}
Xmc11 d11 0 g11 tft_n1_ngspice w={agauss(Wnom,0.40e-6,3)} l={agauss(Lnom,0.15e-6,3)} m={agauss(Mnom,0.08,3)}
Vd12 d12 0 dc={Vd}
Vsh12 g g12 dc={agauss(0,Vshift3s,3)}
Xmc12 d12 0 g12 tft_n1_ngspice w={agauss(Wnom,0.40e-6,3)} l={agauss(Lnom,0.15e-6,3)} m={agauss(Mnom,0.08,3)}
Vd13 d13 0 dc={Vd}
Vsh13 g g13 dc={agauss(0,Vshift3s,3)}
Xmc13 d13 0 g13 tft_n1_ngspice w={agauss(Wnom,0.40e-6,3)} l={agauss(Lnom,0.15e-6,3)} m={agauss(Mnom,0.08,3)}
Vd14 d14 0 dc={Vd}
Vsh14 g g14 dc={agauss(0,Vshift3s,3)}
Xmc14 d14 0 g14 tft_n1_ngspice w={agauss(Wnom,0.40e-6,3)} l={agauss(Lnom,0.15e-6,3)} m={agauss(Mnom,0.08,3)}
Vd15 d15 0 dc={Vd}
Vsh15 g g15 dc={agauss(0,Vshift3s,3)}
Xmc15 d15 0 g15 tft_n1_ngspice w={agauss(Wnom,0.40e-6,3)} l={agauss(Lnom,0.15e-6,3)} m={agauss(Mnom,0.08,3)}

.tran 10n 8u
.print tran v(g) i(vd00)

.control
run
set filetype=ascii
set wr_singlescale
set wr_vecnames
let id00=-i(vd00)
let id01=-i(vd01)
let id02=-i(vd02)
let id03=-i(vd03)
let id04=-i(vd04)
let id05=-i(vd05)
let id06=-i(vd06)
let id07=-i(vd07)
let id08=-i(vd08)
let id09=-i(vd09)
let id10=-i(vd10)
let id11=-i(vd11)
let id12=-i(vd12)
let id13=-i(vd13)
let id14=-i(vd14)
let id15=-i(vd15)
wrdata tft_monte_carlo_idvg.dat v(g) id00 id01 id02 id03 id04 id05 id06 id07 id08 id09 id10 id11 id12 id13 id14 id15
quit
.endc

.end
