FeTFT nf1 Id-Vg Monte Carlo - stock ngspice
* FlexIC-style parallel sampled devices using agauss(...).

.include "../NG_spice_FeTFT/fetft_nf1_vds0p1_ngspice.inc"

.param Vd=0.1
.param VgMin=-5.5
.param VgMax=5.5
.param Vw3s=0.35
.param TableShift3s=0.35
.param Scale3s=0.15
.param Tilt3s=0.18
.temp 27.0
.options method=gear maxord=2

Vgsrc g 0 PWL(0 {VgMin} 1u {VgMin} 12u {VgMax} 13u {VgMax} 24u {VgMin} 25u {VgMin})

Vd00 d00 0 dc={Vd}
Xmc00 g d00 0 fetft_nf1_vds0p1_ngspice pinit=0 vw={agauss(4,Vw3s,3)} scale={agauss(1,Scale3s,3)} hvt_vshift={agauss(0,TableShift3s,3)} lvt_vshift={agauss(0,TableShift3s,3)} hvt_scale={agauss(1,Scale3s,3)} lvt_scale={agauss(1,Scale3s,3)} hvt_tilt={agauss(0,Tilt3s,3)} lvt_tilt={agauss(0,Tilt3s,3)} pol_tau=20n
Vd01 d01 0 dc={Vd}
Xmc01 g d01 0 fetft_nf1_vds0p1_ngspice pinit=0 vw={agauss(4,Vw3s,3)} scale={agauss(1,Scale3s,3)} hvt_vshift={agauss(0,TableShift3s,3)} lvt_vshift={agauss(0,TableShift3s,3)} hvt_scale={agauss(1,Scale3s,3)} lvt_scale={agauss(1,Scale3s,3)} hvt_tilt={agauss(0,Tilt3s,3)} lvt_tilt={agauss(0,Tilt3s,3)} pol_tau=20n
Vd02 d02 0 dc={Vd}
Xmc02 g d02 0 fetft_nf1_vds0p1_ngspice pinit=0 vw={agauss(4,Vw3s,3)} scale={agauss(1,Scale3s,3)} hvt_vshift={agauss(0,TableShift3s,3)} lvt_vshift={agauss(0,TableShift3s,3)} hvt_scale={agauss(1,Scale3s,3)} lvt_scale={agauss(1,Scale3s,3)} hvt_tilt={agauss(0,Tilt3s,3)} lvt_tilt={agauss(0,Tilt3s,3)} pol_tau=20n
Vd03 d03 0 dc={Vd}
Xmc03 g d03 0 fetft_nf1_vds0p1_ngspice pinit=0 vw={agauss(4,Vw3s,3)} scale={agauss(1,Scale3s,3)} hvt_vshift={agauss(0,TableShift3s,3)} lvt_vshift={agauss(0,TableShift3s,3)} hvt_scale={agauss(1,Scale3s,3)} lvt_scale={agauss(1,Scale3s,3)} hvt_tilt={agauss(0,Tilt3s,3)} lvt_tilt={agauss(0,Tilt3s,3)} pol_tau=20n
Vd04 d04 0 dc={Vd}
Xmc04 g d04 0 fetft_nf1_vds0p1_ngspice pinit=0 vw={agauss(4,Vw3s,3)} scale={agauss(1,Scale3s,3)} hvt_vshift={agauss(0,TableShift3s,3)} lvt_vshift={agauss(0,TableShift3s,3)} hvt_scale={agauss(1,Scale3s,3)} lvt_scale={agauss(1,Scale3s,3)} hvt_tilt={agauss(0,Tilt3s,3)} lvt_tilt={agauss(0,Tilt3s,3)} pol_tau=20n
Vd05 d05 0 dc={Vd}
Xmc05 g d05 0 fetft_nf1_vds0p1_ngspice pinit=0 vw={agauss(4,Vw3s,3)} scale={agauss(1,Scale3s,3)} hvt_vshift={agauss(0,TableShift3s,3)} lvt_vshift={agauss(0,TableShift3s,3)} hvt_scale={agauss(1,Scale3s,3)} lvt_scale={agauss(1,Scale3s,3)} hvt_tilt={agauss(0,Tilt3s,3)} lvt_tilt={agauss(0,Tilt3s,3)} pol_tau=20n
Vd06 d06 0 dc={Vd}
Xmc06 g d06 0 fetft_nf1_vds0p1_ngspice pinit=0 vw={agauss(4,Vw3s,3)} scale={agauss(1,Scale3s,3)} hvt_vshift={agauss(0,TableShift3s,3)} lvt_vshift={agauss(0,TableShift3s,3)} hvt_scale={agauss(1,Scale3s,3)} lvt_scale={agauss(1,Scale3s,3)} hvt_tilt={agauss(0,Tilt3s,3)} lvt_tilt={agauss(0,Tilt3s,3)} pol_tau=20n
Vd07 d07 0 dc={Vd}
Xmc07 g d07 0 fetft_nf1_vds0p1_ngspice pinit=0 vw={agauss(4,Vw3s,3)} scale={agauss(1,Scale3s,3)} hvt_vshift={agauss(0,TableShift3s,3)} lvt_vshift={agauss(0,TableShift3s,3)} hvt_scale={agauss(1,Scale3s,3)} lvt_scale={agauss(1,Scale3s,3)} hvt_tilt={agauss(0,Tilt3s,3)} lvt_tilt={agauss(0,Tilt3s,3)} pol_tau=20n
Vd08 d08 0 dc={Vd}
Xmc08 g d08 0 fetft_nf1_vds0p1_ngspice pinit=0 vw={agauss(4,Vw3s,3)} scale={agauss(1,Scale3s,3)} hvt_vshift={agauss(0,TableShift3s,3)} lvt_vshift={agauss(0,TableShift3s,3)} hvt_scale={agauss(1,Scale3s,3)} lvt_scale={agauss(1,Scale3s,3)} hvt_tilt={agauss(0,Tilt3s,3)} lvt_tilt={agauss(0,Tilt3s,3)} pol_tau=20n
Vd09 d09 0 dc={Vd}
Xmc09 g d09 0 fetft_nf1_vds0p1_ngspice pinit=0 vw={agauss(4,Vw3s,3)} scale={agauss(1,Scale3s,3)} hvt_vshift={agauss(0,TableShift3s,3)} lvt_vshift={agauss(0,TableShift3s,3)} hvt_scale={agauss(1,Scale3s,3)} lvt_scale={agauss(1,Scale3s,3)} hvt_tilt={agauss(0,Tilt3s,3)} lvt_tilt={agauss(0,Tilt3s,3)} pol_tau=20n
Vd10 d10 0 dc={Vd}
Xmc10 g d10 0 fetft_nf1_vds0p1_ngspice pinit=0 vw={agauss(4,Vw3s,3)} scale={agauss(1,Scale3s,3)} hvt_vshift={agauss(0,TableShift3s,3)} lvt_vshift={agauss(0,TableShift3s,3)} hvt_scale={agauss(1,Scale3s,3)} lvt_scale={agauss(1,Scale3s,3)} hvt_tilt={agauss(0,Tilt3s,3)} lvt_tilt={agauss(0,Tilt3s,3)} pol_tau=20n
Vd11 d11 0 dc={Vd}
Xmc11 g d11 0 fetft_nf1_vds0p1_ngspice pinit=0 vw={agauss(4,Vw3s,3)} scale={agauss(1,Scale3s,3)} hvt_vshift={agauss(0,TableShift3s,3)} lvt_vshift={agauss(0,TableShift3s,3)} hvt_scale={agauss(1,Scale3s,3)} lvt_scale={agauss(1,Scale3s,3)} hvt_tilt={agauss(0,Tilt3s,3)} lvt_tilt={agauss(0,Tilt3s,3)} pol_tau=20n
Vd12 d12 0 dc={Vd}
Xmc12 g d12 0 fetft_nf1_vds0p1_ngspice pinit=0 vw={agauss(4,Vw3s,3)} scale={agauss(1,Scale3s,3)} hvt_vshift={agauss(0,TableShift3s,3)} lvt_vshift={agauss(0,TableShift3s,3)} hvt_scale={agauss(1,Scale3s,3)} lvt_scale={agauss(1,Scale3s,3)} hvt_tilt={agauss(0,Tilt3s,3)} lvt_tilt={agauss(0,Tilt3s,3)} pol_tau=20n
Vd13 d13 0 dc={Vd}
Xmc13 g d13 0 fetft_nf1_vds0p1_ngspice pinit=0 vw={agauss(4,Vw3s,3)} scale={agauss(1,Scale3s,3)} hvt_vshift={agauss(0,TableShift3s,3)} lvt_vshift={agauss(0,TableShift3s,3)} hvt_scale={agauss(1,Scale3s,3)} lvt_scale={agauss(1,Scale3s,3)} hvt_tilt={agauss(0,Tilt3s,3)} lvt_tilt={agauss(0,Tilt3s,3)} pol_tau=20n
Vd14 d14 0 dc={Vd}
Xmc14 g d14 0 fetft_nf1_vds0p1_ngspice pinit=0 vw={agauss(4,Vw3s,3)} scale={agauss(1,Scale3s,3)} hvt_vshift={agauss(0,TableShift3s,3)} lvt_vshift={agauss(0,TableShift3s,3)} hvt_scale={agauss(1,Scale3s,3)} lvt_scale={agauss(1,Scale3s,3)} hvt_tilt={agauss(0,Tilt3s,3)} lvt_tilt={agauss(0,Tilt3s,3)} pol_tau=20n
Vd15 d15 0 dc={Vd}
Xmc15 g d15 0 fetft_nf1_vds0p1_ngspice pinit=0 vw={agauss(4,Vw3s,3)} scale={agauss(1,Scale3s,3)} hvt_vshift={agauss(0,TableShift3s,3)} lvt_vshift={agauss(0,TableShift3s,3)} hvt_scale={agauss(1,Scale3s,3)} lvt_scale={agauss(1,Scale3s,3)} hvt_tilt={agauss(0,Tilt3s,3)} lvt_tilt={agauss(0,Tilt3s,3)} pol_tau=20n

.tran 20n 25u 0 20n
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
wrdata fetft_monte_carlo_idvg.dat v(g) id00 id01 id02 id03 id04 id05 id06 id07 id08 id09 id10 id11 id12 id13 id14 id15
quit
.endc

.end
