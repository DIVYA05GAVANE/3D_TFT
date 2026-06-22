# Open3DStack padframe geometry and integration constraints.
set ::env(OPEN3DSTACK_DIE_AREA) "0 0 25000 22000"
set ::env(OPEN3DSTACK_USER_AREA) "1000 1000 24000 21000"
set ::env(OPEN3DSTACK_USER_WRAPPER_DIE_AREA) "0 0 23000 20000"
set ::env(OPEN3DSTACK_PAD_COUNT) 184
set ::env(OPEN3DSTACK_PAD_PITCH_UM) 500
set ::env(OPEN3DSTACK_PAD_DEFAULT_KIND) analog
set ::env(OPEN3DSTACK_PAD_MAP) "$::env(DESIGN_DIR)/../../open3dstack/constraints/open3dstack_pads.csv"
set ::env(OPEN3DSTACK_PIN_ORDER_CFG) "$::env(DESIGN_DIR)/../../open3dstack/constraints/open3dstack_user_project_wrapper.pin_order.cfg"
