*  Generated for: HSPICE
*  Generated on: Jun 17 18:35:53 2026
*  Design library name: CAM_Circuits
*  Design cell name: tb_precharge
*  Design view name: schematic
.include '/apps/PDK/NCSU/FreePDK/FreePDK45/1.4/ncsu_basekit/models/hspice/hspice_nom.include'
*  Library name: CAM_Circuits
*  Cell name: nfet_W6u_L5
*  View name: schematic
.subckt nfet_w6u_l5 d g s
    m0 d g s s NMOS_VTG L=5e-6 W=6e-6 AD=630e-15 AS=630e-15 PD=6.21e-6 PS=6.21e-6 M=1
.ends
*  End of subcircuit definition.
*  Library name: CAM_Circuits
*  Cell name: precharge_equalizer_nmos_6u
*  View name: schematic
.subckt precharge_equalizer_nmos_6u bl blb eq pchg vdd vpre
    xi28 bl eq blb nfet_w6u_l5
    xi27 bl eq blb nfet_w6u_l5
    xi26 net10 pchg blb nfet_w6u_l5
    xi25 net10 pchg blb nfet_w6u_l5
    xi24 net10 pchg bl nfet_w6u_l5
    xi23 net10 pchg bl nfet_w6u_l5
    xi22 vdd vpre net10 nfet_w6u_l5
    xi21 vdd vpre net10 nfet_w6u_l5
.ends
*  End of subcircuit definition.

*  Library name: CAM_Circuits
*  Cell name: tb_precharge
*  View name: schematic
xi4 bl blb eq net06 vdd pchg precharge_equalizer_nmos_6u
c1 bl 0 c=200e-12 ic=0
c0 blb 0 c=100e-12 ic=0
r1 bl 0 r=100e3
r0 blb 0 r=50e3
v1 net06 0 dc=3.5
v0 vdd 0 dc=2
v3 pchg 0 PULSE ( 3 0 0 100e-9 100e-9 10e-6 20e-6 )
v2 eq 0 PULSE ( 0 3 0 100e-9 100e-9 10e-6 20e-6 )
.temp 27.0
.option GEN_CUR_POL=ON
.option ARTIST=2 PSF=2 WARN_SEP=1
.option VECBUS=1 LIS_NEW=1 CONVERGE=100
.tran 10e-9 50e-6 start=0.0
.option hier_delim=1
.probe tran v(bl)
+       v(blb)
+       v(eq)
+       v(pchg)
+       v(vdd)
+       i(c0)
+       i(r0)
+       i(r1)
+       i(v0)
.end
