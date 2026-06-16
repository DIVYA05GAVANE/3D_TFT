*  Generated for: HSPICE
*  Generated on: Jun 16 21:51:49 2026
*  Design library name: CAM_Circuits
*  Design cell name: tb_sense_amp
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
*  Cell name: nfet_W24u_L5
*  View name: schematic
.subckt nfet_w24u_l5 d g s
+   l=5e-6 w=24e-6 m=1
    m0 d g s s NMOS_VTG L=l W=w AD=2.52e-12 AS=2.52e-12 PD=24.21e-6 PS=24.21e-6 M=m
.ends
*  End of subcircuit definition.
*  Library name: CAM_Circuits
*  Cell name: nfet_W20p825_L5
*  View name: schematic
.subckt nfet_w20p825_l5 d g s
+   l=5e-6 w=20.825e-6 m=1
    m0 d g s s NMOS_VTG L=l W=w AD=2.18663e-12 AS=2.18663e-12 PD=21.035e-6 PS=21.035e-6 M=m
.ends
*  End of subcircuit definition.
*  Library name: CAM_Circuits
*  Cell name: INV_X4PC_T5_nmos
*  View name: schematic
.subckt inv_x4pc_t5_nmos in out vdd vss
    xi10 vdd vdd an nfet_w24u_l5 m=1 l=5e-6 w=24e-6 m=1
    xi6 an in vss nfet_w20p825_l5 m=4 l=5e-6 w=20.825e-6 m=4
    xi8 out in vss nfet_w20p825_l5 m=8 l=5e-6 w=20.825e-6 m=8
    xi7 vdd an out nfet_w20p825_l5 m=8 l=5e-6 w=20.825e-6 m=8
.ends
*  End of subcircuit definition.
*  Library name: CAM_Circuits
*  Cell name: opamp_6u
*  View name: schematic
.subckt opamp_6u out_inv sl slb vdd vdd_inv vss vth
    xi31 slb sl vss nfet_w6u_l5
    xi30 slb sl vss nfet_w6u_l5
    xi29 sl sl vss nfet_w6u_l5
    xi28 sl sl vss nfet_w6u_l5
    xi25 vdd vth sl nfet_w6u_l5
    xi24 vdd vth sl nfet_w6u_l5
    xi17 slb out_inv vdd_inv vss inv_x4pc_t5_nmos
.ends
*  End of subcircuit definition.

*  Library name: CAM_Circuits
*  Cell name: tb_sense_amp
*  View name: schematic
xi0 out sl slb vdd vdd_inv 0 vth opamp_6u
i7 0 slb PULSE ( 60e-6 40e-6 0 100e-9 100e-9 10e-6 20e-6 )
i5 0 sl PULSE ( 40e-6 60e-6 0 100e-9 100e-9 10e-6 20e-6 )
v2 vdd 0 dc=2
v1 vdd_inv 0 dc=1.7
v0 vth 0 dc=2.05
c0 out 0 c=1e-12
.temp 27.0
.option GEN_CUR_POL=ON
.option ARTIST=2 PSF=2 WARN_SEP=1
.option VECBUS=1 LIS_NEW=1 CONVERGE=100
.tran 10e-9 40e-6 start=0.0
.option hier_delim=1
.probe tran v(out)
+       v(sl)
+       v(slb)
+       v(vdd)
+       v(vdd_inv)
+       v(vth)
+       i(v0)
+       i(v1)
+       i(v2)
.end
