# OpenLane template for an Open3DStack user project wrapper.
set design_dir $::env(DESIGN_DIR)
set macro_lib "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/tft3d_macros"

set ::env(DESIGN_NAME) open3dstack_user_project_wrapper
set ::env(DESIGN_IS_CORE) 0

set ::env(VERILOG_FILES) [list \
    "$design_dir/../../open3dstack/verilog/open3dstack_user_defines.v" \
    "$design_dir/src/open3dstack_user_project_wrapper.v" \
]
set ::env(VERILOG_FILES_BLACKBOX) [list \
    "$macro_lib/verilog/open3dstack_frame_blackboxes.v" \
]
set ::env(EXTRA_LEFS) [list \
    "$macro_lib/lef/open3dstack_padframe.lef" \
    "$macro_lib/lef/wl_pad.lef" \
]
set ::env(EXTRA_GDS_FILES) [list \
    "$macro_lib/gds/open3dstack_padframe.gds" \
    "$macro_lib/gds/wl_pad.gds" \
]

set ::env(CLOCK_PORT) ""
set ::env(CLOCK_PERIOD) 10
set ::env(RUN_CTS) 0

set ::env(FP_SIZING) absolute
set ::env(DIE_AREA) "0 0 23000 20000"
set ::env(CORE_AREA) "100 100 22900 19900"
set ::env(FP_PIN_ORDER_CFG) "$design_dir/pin_order.cfg"
set ::env(PL_TARGET_DENSITY) 0.05

set ::env(FP_PDN_ENABLE_RAILS) 0
set ::env(FP_PDN_ENABLE_MACROS_GRID) 0
set ::env(RUN_LVS) 0
set ::env(RUN_CVC) 0
set ::env(RUN_MAGIC) 0
set ::env(RUN_MAGIC_DRC) 0
set ::env(RUN_KLAYOUT_DRC) 0
set ::env(RUN_KLAYOUT_XOR) 0
