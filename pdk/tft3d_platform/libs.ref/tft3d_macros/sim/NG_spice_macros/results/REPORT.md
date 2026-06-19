# NG-spice macro simulation report

Run this suite from `pdk/tft3d_platform/libs.ref/tft3d_macros/sim/NG_spice_macros` with `./run_all.sh`.

Pass: 29
Fail: 0
Skipped physical/empty: 9

## Passed Decks
- `3d_inv_x4pc_transfer` (3d_tft_macros.spice) rows=701 dat=`results/3d_inv_x4pc_transfer.dat`
- `3d_nand3_x4rl_transfer_a1` (3d_tft_macros.spice) rows=701 dat=`results/3d_nand3_x4rl_transfer_a1.dat`
- `3d_nfet_W20p825_L5_idvds_vg3` (3d_tft_macros.spice) rows=801 dat=`results/3d_nfet_W20p825_L5_idvds_vg3.dat`
- `3d_nfet_W24u_L5_idvds_vg3` (3d_tft_macros.spice) rows=801 dat=`results/3d_nfet_W24u_L5_idvds_vg3.dat`
- `3d_nfet_W6u_L5_idvds_vg3` (3d_tft_macros.spice) rows=801 dat=`results/3d_nfet_W6u_L5_idvds_vg3.dat`
- `3d_wl_inv_transfer` (3d_tft_macros.spice) rows=701 dat=`results/3d_wl_inv_transfer.dat`
- `3d_wl_prebuffer_transfer` (3d_tft_macros.spice) rows=701 dat=`results/3d_wl_prebuffer_transfer.dat`
- `3d_wl_sel_transfer` (3d_tft_macros.spice) rows=701 dat=`results/3d_wl_sel_transfer.dat`
- `analog_mux_2to1_diff_schematic_tran` (analog_mux_2to1_diff_nmos.spice) rows=548 dat=`results/analog_mux_2to1_diff_schematic_tran.dat`
- `analog_mux_2to1_diff_tran` (analog_mux_2to1_diff_nmos.spice) rows=548 dat=`results/analog_mux_2to1_diff_tran.dat`
- `analog_mux_bl_sl_tran` (analog_mux_bl_sl_nmos.spice) rows=546 dat=`results/analog_mux_bl_sl_tran.dat`
- `column_decoder_3to8_tran` (column_decoder_3to8_nmos.spice) rows=970 dat=`results/column_decoder_3to8_tran.dat`
- `inv_x4pc_transfer` (peripheral_ic.spice) rows=701 dat=`results/inv_x4pc_transfer.dat`
- `nand3_x4rl_transfer_a1` (peripheral_ic.spice) rows=701 dat=`results/nand3_x4rl_transfer_a1.dat`
- `nand3_x4rl_truth_tran` (peripheral_ic.spice) rows=939 dat=`results/nand3_x4rl_truth_tran.dat`
- `nfet_w20p825_l5_idvds_vg3` (generated/native_tft) rows=801 dat=`results/nfet_w20p825_l5_idvds_vg3.dat`
- `nfet_w24u_l5_idvds_vg3` (generated/native_tft) rows=801 dat=`results/nfet_w24u_l5_idvds_vg3.dat`
- `nfet_w6u_l5_idvds_vg3` (generated/native_tft) rows=801 dat=`results/nfet_w6u_l5_idvds_vg3.dat`
- `nfet_w6u_l5_idvg_vd0p1` (generated/native_tft) rows=601 dat=`results/nfet_w6u_l5_idvg_vd0p1.dat`
- `nfet_w6u_l5_idvg_vd2p0` (generated/native_tft) rows=601 dat=`results/nfet_w6u_l5_idvg_vd2p0.dat`
- `opamp_6u_sense_tran` (tb_sense_amp.sp) rows=2029 dat=`results/opamp_6u_sense_tran.dat`
- `peripheral_ic_top_smoke_tran` (peripheral_ic.spice) rows=364 dat=`results/peripheral_ic_top_smoke_tran.dat`
- `precharge_equalizer_tran` (tb_precharge.sp) rows=2538 dat=`results/precharge_equalizer_tran.dat`
- `row_decoder_3to8_tran` (row_decoder_3to8_nmos.spice) rows=970 dat=`results/row_decoder_3to8_tran.dat`
- `wl_driver_nmos_tran` (peripheral_ic.spice) rows=648 dat=`results/wl_driver_nmos_tran.dat`
- `wl_inv_transfer` (peripheral_ic.spice) rows=701 dat=`results/wl_inv_transfer.dat`
- `wl_prebuffer_transfer` (peripheral_ic.spice) rows=701 dat=`results/wl_prebuffer_transfer.dat`
- `wl_sel_tran` (peripheral_ic.spice) rows=655 dat=`results/wl_sel_tran.dat`
- `write_driver_tran` (column_driver.spice) rows=2309 dat=`results/write_driver_tran.dat`

## Failed Decks
- none

## Skipped
- `stack_sram_array_f0`: Subckt is empty/physical-only in source netlist; no meaningful electrical output to plot.
- `stack_sram_array_f1`: Subckt is empty/physical-only in source netlist; no meaningful electrical output to plot.
- `stack_sram_array_f2`: Subckt is empty/physical-only in source netlist; no meaningful electrical output to plot.
- `stack_sram_array_f3`: Subckt is empty/physical-only in source netlist; no meaningful electrical output to plot.
- `stack_sram_array_f4`: Subckt is empty/physical-only in source netlist; no meaningful electrical output to plot.
- `stack_sram_array_f5`: Subckt is empty/physical-only in source netlist; no meaningful electrical output to plot.
- `wl_pad`: Subckt is empty/physical-only in source netlist; no meaningful electrical output to plot.
- `open3dstack_padframe`: Subckt is empty/physical-only in source netlist; no meaningful electrical output to plot.
- `open3dstack_user_project_wrapper`: Subckt is empty/physical-only in source netlist; no meaningful electrical output to plot.

## Plot Files
- `plots/3d_inv_x4pc_transfer.svg`
- `plots/3d_nand3_x4rl_transfer_a1.svg`
- `plots/3d_nfet_W20p825_L5_idvds_vg3.svg`
- `plots/3d_nfet_W24u_L5_idvds_vg3.svg`
- `plots/3d_nfet_W6u_L5_idvds_vg3.svg`
- `plots/3d_wl_inv_transfer.svg`
- `plots/3d_wl_prebuffer_transfer.svg`
- `plots/3d_wl_sel_transfer.svg`
- `plots/analog_mux_2to1_diff_schematic_tran.svg`
- `plots/analog_mux_2to1_diff_tran.svg`
- `plots/analog_mux_bl_sl_tran.svg`
- `plots/column_decoder_3to8_tran.svg`
- `plots/inv_x4pc_transfer.svg`
- `plots/nand3_x4rl_transfer_a1.svg`
- `plots/nand3_x4rl_truth_tran.svg`
- `plots/nfet_family_idvds_overlay.svg`
- `plots/nfet_w20p825_l5_idvds_vg3.svg`
- `plots/nfet_w24u_l5_idvds_vg3.svg`
- `plots/nfet_w6u_l5_idvds_vg3.svg`
- `plots/nfet_w6u_l5_idvg_vd0p1.svg`
- `plots/nfet_w6u_l5_idvg_vd2p0.svg`
- `plots/opamp_6u_sense_tran.svg`
- `plots/peripheral_ic_top_smoke_tran.svg`
- `plots/precharge_equalizer_tran.svg`
- `plots/row_decoder_3to8_tran.svg`
- `plots/wl_driver_nmos_tran.svg`
- `plots/wl_inv_transfer.svg`
- `plots/wl_prebuffer_transfer.svg`
- `plots/wl_sel_tran.svg`
- `plots/write_driver_tran.svg`
