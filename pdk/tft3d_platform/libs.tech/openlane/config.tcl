# Neutral local OpenLane PDK wrapper for the 3D_TFT platform assets.

set ::env(PROCESS) 45
set ::env(DEF_UNITS_PER_MICRON) 1000

if { ![info exist ::env(STD_CELL_LIBRARY)] } {
    set ::env(STD_CELL_LIBRARY) tft3d_sc_t5
}
if { ![info exist ::env(STD_CELL_LIBRARY_OPT)] } {
    set ::env(STD_CELL_LIBRARY_OPT) tft3d_sc_t5
}

set ::env(VDD_PIN) VDD
set ::env(GND_PIN) VSS
set ::env(VDD_PIN_VOLTAGE) 1.50
set ::env(GND_PIN_VOLTAGE) 0.00
set ::env(STD_CELL_POWER_PINS) VDD
set ::env(STD_CELL_GROUND_PINS) VSS

set ::env(TECH_LEF) "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/techlef/tft3d_platform.tlef"
set ::env(TECH_LEF_MIN) $::env(TECH_LEF)
set ::env(TECH_LEF_MAX) $::env(TECH_LEF)
set ::env(CELLS_LEF) [list     "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/lef/tft3d_sc_t5_sites.lef"     "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/lef/tft3d_sc_t5.lef" ]
set ::env(GDS_FILES) [glob "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/gds/*.gds"]
set ::env(STD_CELL_LIBRARY_CDL) "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/cdl/tft3d_sc_t5.cdl"
set ::env(SPICE_MODEL_FILES) [list \
    "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/ngspice/tft3d_platform.spice" \
]
set ::env(SPICE_PRIMITIVE_MODELS) [list \
    "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/ngspice/tft3d_platform_primitives.spice" \
]
set ::env(STD_CELL_SPICE) "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/spice/tft3d_sc_t5.spice"
set ::env(SIMULATION_MANIFEST) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/openflow/simulation.yml"
set ::env(TFT3D_MACRO_LIBRARY) "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/tft3d_macros"
set ::env(TFT3D_MACRO_LEFS) [glob "$::env(TFT3D_MACRO_LIBRARY)/lef/*.lef"]
set ::env(TFT3D_MACRO_GDS_FILES) [glob "$::env(TFT3D_MACRO_LIBRARY)/gds/*.gds"]
set ::env(TFT3D_MACRO_LIB) "$::env(TFT3D_MACRO_LIBRARY)/lib/3d_tft_placeholders.lib"
set ::env(TFT3D_MACRO_SPICE) "$::env(TFT3D_MACRO_LIBRARY)/spice/3d_tft_macros.spice"
set ::env(TFT3D_MACRO_BLACKBOXES) "$::env(TFT3D_MACRO_LIBRARY)/verilog/3d_tft_blackboxes.v"

set ::env(TECH_LEF_OPT) $::env(TECH_LEF)
set ::env(CELLS_LEF_OPT) $::env(CELLS_LEF)
set ::env(GDS_FILES_OPT) $::env(GDS_FILES)
set ::env(STD_CELL_LIBRARY_OPT_CDL) $::env(STD_CELL_LIBRARY_CDL)

source "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/openlane/$::env(STD_CELL_LIBRARY)/config.tcl"
set ::env(LIB_SLOWEST_OPT) $::env(LIB_SLOWEST)

set ::env(KLAYOUT_TECH) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/klayout/tech/tft3d_platform.lyt"
set ::env(KLAYOUT_PROPERTIES) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/klayout/tech/tft3d_platform.lyp"
set ::env(KLAYOUT_DEF_LAYER_MAP) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/klayout/tech/tft3d_platform.map"

set ::env(TRACKS_INFO_FILE) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/openlane/$::env(STD_CELL_LIBRARY)/tracks.info"
set ::env(NO_SYNTH_CELL_LIST) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/openlane/$::env(STD_CELL_LIBRARY)/no_synth.cells"
set ::env(DRC_EXCLUDE_CELL_LIST) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/openlane/$::env(STD_CELL_LIBRARY)/drc_exclude.cells"
set ::env(DRC_EXCLUDE_CELL_LIST_OPT) $::env(DRC_EXCLUDE_CELL_LIST)

set ::env(FP_PDN_RAIL_LAYER) SD
set ::env(FP_PDN_VERTICAL_LAYER) MT1
set ::env(FP_PDN_HORIZONTAL_LAYER) MT2
set ::env(FP_PDN_RAIL_OFFSET) 0
set ::env(FP_PDN_RAIL_WIDTH) 1
set ::env(FP_PDN_VWIDTH) 1
set ::env(FP_PDN_HWIDTH) 1
set ::env(FP_PDN_VSPACING) 1
set ::env(FP_PDN_HSPACING) 1
set ::env(FP_PDN_VOFFSET) 500
set ::env(FP_PDN_HOFFSET) 500
set ::env(FP_PDN_VPITCH) 5000
set ::env(FP_PDN_HPITCH) 5000
set ::env(MACRO_BLOCKAGES_LAYER) "SD GATE MT1 MT2"

set ::env(DATA_WIRE_RC_LAYER) MT2
set ::env(CLOCK_WIRE_RC_LAYER) MT2
set ::env(FP_IO_HLAYER) MT2
set ::env(FP_IO_VLAYER) MT1
set ::env(RT_MIN_LAYER) MT1
set ::env(RT_MAX_LAYER) MT2
set ::env(RT_CLOCK_MIN_LAYER) MT1
set ::env(GRT_LAYER_ADJUSTMENTS) "0,0"
