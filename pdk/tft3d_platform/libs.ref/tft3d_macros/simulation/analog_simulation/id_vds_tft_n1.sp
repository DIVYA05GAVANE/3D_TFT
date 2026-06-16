*  Generated for: HSPICE
*  Generated on: Jun 16 12:52:00 2026
*  Design library name: CAM_Circuits
*  Design cell name: opamp
*  Design view name: schematic
.include '/apps/PDK/NCSU/FreePDK/FreePDK45/1.4/ncsu_basekit/models/hspice/hspice_nom.include'

*  Library name: CAM_Circuits
*  Cell name: opamp
*  View name: schematic
xi7 vd vs vg tft_n1
v2 vs 0 dc=0
v1 vd 0 dc='Vd'
v0 vg 0 dc='Vg'
.param
+   Vg=3
+   Vd=0
.temp 27.0
.option GEN_CUR_POL=ON
.option ARTIST=2 PSF=2 WARN_SEP=1
.option VECBUS=1 LIS_NEW=1 CONVERGE=100
.dc Vd -3.0 5.0 10e-3
.option hier_delim=1
.probe dc i(xi7.d)
.hdl "tft_n1.va"
.end
