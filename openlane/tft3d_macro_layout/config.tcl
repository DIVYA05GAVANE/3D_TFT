# OpenLane layout target for the 3D_TFT hard-macro package.
# Uses the repo-local tft3d_platform PDK and platform-layer macro views.

set design_dir $::env(DESIGN_DIR)
set macro_lib "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/tft3d_macros"

set ::env(DESIGN_NAME) tft3d_macro_layout
set ::env(DESIGN_IS_CORE) 0

set ::env(VERILOG_FILES) [list \
    "$design_dir/src/tft3d_macro_layout.v" \
]
set ::env(VERILOG_FILES_BLACKBOX) [list \
    "$macro_lib/verilog/3d_tft_blackboxes.v" \
]
set ::env(EXTRA_LEFS) [glob "$macro_lib/lef/*.lef"]
set ::env(EXTRA_GDS_FILES) [glob "$macro_lib/gds/*.gds"]
set ::env(EXTRA_LIBS) [list \
    "$macro_lib/lib/3d_tft_placeholders.lib" \
]
set ::env(EXTRA_SPICE_FILES) [list \
    "$macro_lib/spice/3d_tft_macros.spice" \
]

set ::env(CLOCK_PORT) ""
set ::env(CLOCK_PERIOD) 10
set ::env(RUN_CTS) 0

set ::env(FP_SIZING) absolute
set ::env(DIE_AREA) "0 0 6600 4300"
set ::env(CORE_AREA) "40 40 6560 4260"
set ::env(FP_PIN_ORDER_CFG) "$design_dir/pin_order.cfg"
set ::env(MACRO_PLACEMENT_CFG) "$design_dir/macro_placement.cfg"
set ::env(PL_TARGET_DENSITY) 0.05

set ::env(FP_PDN_AUTO_ADJUST) 0
set ::env(FP_PDN_SKIPTRIM) 1
set ::env(FP_PDN_CHECK_NODES) 0
set ::env(FP_PDN_ENABLE_RAILS) 0
set ::env(FP_PDN_ENABLE_MACROS_GRID) 0
set ::env(FP_PDN_VPITCH) 5000
set ::env(FP_PDN_HPITCH) 5000
set ::env(FP_PDN_VOFFSET) 500
set ::env(FP_PDN_HOFFSET) 500

set ::env(KLAYOUT_DEF_LAYER_MAP) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/klayout/tech/tft3d_platform.map"
set ::env(PRIMARY_SIGNOFF_TOOL) klayout
set ::env(RUN_KLAYOUT) 1
set ::env(RUN_MAGIC) 0
set ::env(RUN_MAGIC_DRC) 0
set ::env(RUN_KLAYOUT_DRC) 0
set ::env(RUN_KLAYOUT_XOR) 0
set ::env(RUN_LVS) 0
set ::env(RUN_CVC) 0
set ::env(RUN_SPEF_EXTRACTION) 0
set ::env(RUN_IRDROP_REPORT) 0
set ::env(RUN_TAP_DECAP_INSERTION) 0
set ::env(RUN_FILL_INSERTION) 0

set ::env(PL_ESTIMATE_PARASITICS) 0
set ::env(GRT_ESTIMATE_PARASITICS) 0
set ::env(PL_RESIZER_DESIGN_OPTIMIZATIONS) 0
set ::env(PL_RESIZER_TIMING_OPTIMIZATIONS) 0
set ::env(GLB_RESIZER_DESIGN_OPTIMIZATIONS) 0
set ::env(GLB_RESIZER_TIMING_OPTIMIZATIONS) 0
set ::env(PL_RESIZER_BUFFER_INPUT_PORTS) 0
set ::env(PL_RESIZER_BUFFER_OUTPUT_PORTS) 0
set ::env(PL_RESIZER_REPAIR_TIE_FANOUT) 0
set ::env(GRT_REPAIR_ANTENNAS) 0
set ::env(RUN_HEURISTIC_DIODE_INSERTION) 0

set ::env(FP_IO_HLAYER) MT2
set ::env(FP_IO_VLAYER) MT1
set ::env(RT_MIN_LAYER) MT1
set ::env(RT_MAX_LAYER) MT2
set ::env(RT_CLOCK_MIN_LAYER) MT1

set ::env(QUIT_ON_TR_DRC) 0
set ::env(QUIT_ON_TIMING_VIOLATIONS) 0
set ::env(QUIT_ON_MAGIC_DRC) 0
set ::env(QUIT_ON_LVS_ERROR) 0
set ::env(QUIT_ON_UNMAPPED_CELLS) 0
