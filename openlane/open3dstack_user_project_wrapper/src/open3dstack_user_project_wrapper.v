`ifndef PERIPHERAL_IC_BLACKBOX_V
`define PERIPHERAL_IC_BLACKBOX_V

(* blackbox *)
module peripheral_ic (
    inout wire vdd_driver_wl,
    inout wire vss_driver_wl,
    inout wire vwl_p_wl_driver,
    inout wire vwl_n_wl_driver,
    inout wire vdd_decoder_wl,
    inout wire vdda_decoder_wl,
    inout wire vss_decoder_wl,
    inout wire vssa_decoder_wl,
    inout wire d0,
    inout wire d1,
    inout wire d2,
    inout wire d3,
    inout wire d4,
    inout wire d5,
    inout wire d6,
    inout wire d7,
    inout wire d8,
    inout wire d9,
    inout wire d10,
    inout wire d11,
    inout wire co,
    inout wire c1,
    inout wire c2,
    inout wire we,
    inout wire wl_in,
    inout wire net097,
    inout wire net0118,
    inout wire net094,
    inout wire net0100,
    inout wire net098,
    inout wire net099,
    inout wire vdd_column_decoder,
    inout wire vdda_column_decoder,
    inout wire vss_column_decoder,
    inout wire vssa_column_decoder,
    inout wire vdd_column_driver,
    inout wire vdda_column_driver,
    inout wire vphb_bl_column_driver,
    inout wire vphb_sl_column_driver,
    inout wire vph_bl_column_driver,
    inout wire vph_sl_column_driver,
    inout wire vplb_bl_column_decoder,
    inout wire vplb_sl_column_decoder,
    inout wire vpl_bl_column_decoder,
    inout wire vpl_sl_column_decoder,
    inout wire precharge,
    inout wire vpre,
    inout wire eq,
    inout wire pchg,
    inout wire sel_mux,
    inout wire selb_mux,
    inout wire vdd_sense,
    inout wire vdd_inv_sense,
    inout wire vss_sense,
    inout wire vth_sense,
    inout wire \sense_out<0> ,
    inout wire \sense_out<1> ,
    inout wire \sense_out<2> ,
    inout wire \sense_out<3> ,
    inout wire \sense_out<4> ,
    inout wire \sense_out<5> ,
    inout wire \sense_out<6> ,
    inout wire \sense_out<7>
);
endmodule

`endif

module open3dstack_user_project_wrapper (
    inout wire PAD_S00,
    inout wire PAD_S01,
    inout wire PAD_S02,
    inout wire PAD_S03,
    inout wire PAD_S04,
    inout wire PAD_S05,
    inout wire PAD_S06,
    inout wire PAD_S07,
    inout wire PAD_S08,
    inout wire PAD_S09,
    inout wire PAD_S10,
    inout wire PAD_S11,
    inout wire PAD_S12,
    inout wire PAD_S13,
    inout wire PAD_S14,
    inout wire PAD_S15,
    inout wire PAD_S16,
    inout wire PAD_S17,
    inout wire PAD_S18,
    inout wire PAD_S19,
    inout wire PAD_S20,
    inout wire PAD_S21,
    inout wire PAD_S22,
    inout wire PAD_S23,
    inout wire PAD_S24,
    inout wire PAD_S25,
    inout wire PAD_S26,
    inout wire PAD_S27,
    inout wire PAD_S28,
    inout wire PAD_S29,
    inout wire PAD_S30,
    inout wire PAD_S31,
    inout wire PAD_S32,
    inout wire PAD_S33,
    inout wire PAD_S34,
    inout wire PAD_S35,
    inout wire PAD_S36,
    inout wire PAD_S37,
    inout wire PAD_S38,
    inout wire PAD_S39,
    inout wire PAD_S40,
    inout wire PAD_S41,
    inout wire PAD_S42,
    inout wire PAD_S43,
    inout wire PAD_S44,
    inout wire PAD_S45,
    inout wire PAD_S46,
    inout wire PAD_S47,
    inout wire PAD_S48,
    inout wire PAD_E00,
    inout wire PAD_E01,
    inout wire PAD_E02,
    inout wire PAD_E03,
    inout wire PAD_E04,
    inout wire PAD_E05,
    inout wire PAD_E06,
    inout wire PAD_E07,
    inout wire PAD_E08,
    inout wire PAD_E09,
    inout wire PAD_E10,
    inout wire PAD_E11,
    inout wire PAD_E12,
    inout wire PAD_E13,
    inout wire PAD_E14,
    inout wire PAD_E15,
    inout wire PAD_E16,
    inout wire PAD_E17,
    inout wire PAD_E18,
    inout wire PAD_E19,
    inout wire PAD_E20,
    inout wire PAD_E21,
    inout wire PAD_E22,
    inout wire PAD_E23,
    inout wire PAD_E24,
    inout wire PAD_E25,
    inout wire PAD_E26,
    inout wire PAD_E27,
    inout wire PAD_E28,
    inout wire PAD_E29,
    inout wire PAD_E30,
    inout wire PAD_E31,
    inout wire PAD_E32,
    inout wire PAD_E33,
    inout wire PAD_E34,
    inout wire PAD_E35,
    inout wire PAD_E36,
    inout wire PAD_E37,
    inout wire PAD_E38,
    inout wire PAD_E39,
    inout wire PAD_E40,
    inout wire PAD_E41,
    inout wire PAD_E42,
    inout wire PAD_N00,
    inout wire PAD_N01,
    inout wire PAD_N02,
    inout wire PAD_N03,
    inout wire PAD_N04,
    inout wire PAD_N05,
    inout wire PAD_N06,
    inout wire PAD_N07,
    inout wire PAD_N08,
    inout wire PAD_N09,
    inout wire PAD_N10,
    inout wire PAD_N11,
    inout wire PAD_N12,
    inout wire PAD_N13,
    inout wire PAD_N14,
    inout wire PAD_N15,
    inout wire PAD_N16,
    inout wire PAD_N17,
    inout wire PAD_N18,
    inout wire PAD_N19,
    inout wire PAD_N20,
    inout wire PAD_N21,
    inout wire PAD_N22,
    inout wire PAD_N23,
    inout wire PAD_N24,
    inout wire PAD_N25,
    inout wire PAD_N26,
    inout wire PAD_N27,
    inout wire PAD_N28,
    inout wire PAD_N29,
    inout wire PAD_N30,
    inout wire PAD_N31,
    inout wire PAD_N32,
    inout wire PAD_N33,
    inout wire PAD_N34,
    inout wire PAD_N35,
    inout wire PAD_N36,
    inout wire PAD_N37,
    inout wire PAD_N38,
    inout wire PAD_N39,
    inout wire PAD_N40,
    inout wire PAD_N41,
    inout wire PAD_N42,
    inout wire PAD_N43,
    inout wire PAD_N44,
    inout wire PAD_N45,
    inout wire PAD_N46,
    inout wire PAD_N47,
    inout wire PAD_N48,
    inout wire PAD_W00,
    inout wire PAD_W01,
    inout wire PAD_W02,
    inout wire PAD_W03,
    inout wire PAD_W04,
    inout wire PAD_W05,
    inout wire PAD_W06,
    inout wire PAD_W07,
    inout wire PAD_W08,
    inout wire PAD_W09,
    inout wire PAD_W10,
    inout wire PAD_W11,
    inout wire PAD_W12,
    inout wire PAD_W13,
    inout wire PAD_W14,
    inout wire PAD_W15,
    inout wire PAD_W16,
    inout wire PAD_W17,
    inout wire PAD_W18,
    inout wire PAD_W19,
    inout wire PAD_W20,
    inout wire PAD_W21,
    inout wire PAD_W22,
    inout wire PAD_W23,
    inout wire PAD_W24,
    inout wire PAD_W25,
    inout wire PAD_W26,
    inout wire PAD_W27,
    inout wire PAD_W28,
    inout wire PAD_W29,
    inout wire PAD_W30,
    inout wire PAD_W31,
    inout wire PAD_W32,
    inout wire PAD_W33,
    inout wire PAD_W34,
    inout wire PAD_W35,
    inout wire PAD_W36,
    inout wire PAD_W37,
    inout wire PAD_W38,
    inout wire PAD_W39,
    inout wire PAD_W40,
    inout wire PAD_W41,
    inout wire PAD_W42
);
    wire vdd_driver_wl;
    wire vss_driver_wl;
    wire vwl_p_wl_driver;
    wire vwl_n_wl_driver;
    wire vdd_decoder_wl;
    wire vdda_decoder_wl;
    wire vss_decoder_wl;
    wire vssa_decoder_wl;
    wire d0;
    wire d1;
    wire d2;
    wire d3;
    wire d4;
    wire d5;
    wire d6;
    wire d7;
    wire d8;
    wire d9;
    wire d10;
    wire d11;
    wire co;
    wire c1;
    wire c2;
    wire we;
    wire wl_in;
    wire net097;
    wire net0118;
    wire net094;
    wire net0100;
    wire net098;
    wire net099;
    wire vdd_column_decoder;
    wire vdda_column_decoder;
    wire vss_column_decoder;
    wire vssa_column_decoder;
    wire vdd_column_driver;
    wire vdda_column_driver;
    wire vphb_bl_column_driver;
    wire vphb_sl_column_driver;
    wire vph_bl_column_driver;
    wire vph_sl_column_driver;
    wire vplb_bl_column_decoder;
    wire vplb_sl_column_decoder;
    wire vpl_bl_column_decoder;
    wire vpl_sl_column_decoder;
    wire precharge;
    wire vpre;
    wire eq;
    wire pchg;
    wire sel_mux;
    wire selb_mux;
    wire vdd_sense;
    wire vdd_inv_sense;
    wire vss_sense;
    wire vth_sense;
    wire \sense_out<0> ;
    wire \sense_out<1> ;
    wire \sense_out<2> ;
    wire \sense_out<3> ;
    wire \sense_out<4> ;
    wire \sense_out<5> ;
    wire \sense_out<6> ;
    wire \sense_out<7> ;

    peripheral_ic u_peripheral_ic (
        .vdd_driver_wl(vdd_driver_wl),
        .vss_driver_wl(vss_driver_wl),
        .vwl_p_wl_driver(vwl_p_wl_driver),
        .vwl_n_wl_driver(vwl_n_wl_driver),
        .vdd_decoder_wl(vdd_decoder_wl),
        .vdda_decoder_wl(vdda_decoder_wl),
        .vss_decoder_wl(vss_decoder_wl),
        .vssa_decoder_wl(vssa_decoder_wl),
        .d0(d0),
        .d1(d1),
        .d2(d2),
        .d3(d3),
        .d4(d4),
        .d5(d5),
        .d6(d6),
        .d7(d7),
        .d8(d8),
        .d9(d9),
        .d10(d10),
        .d11(d11),
        .co(co),
        .c1(c1),
        .c2(c2),
        .we(we),
        .wl_in(wl_in),
        .net097(net097),
        .net0118(net0118),
        .net094(net094),
        .net0100(net0100),
        .net098(net098),
        .net099(net099),
        .vdd_column_decoder(vdd_column_decoder),
        .vdda_column_decoder(vdda_column_decoder),
        .vss_column_decoder(vss_column_decoder),
        .vssa_column_decoder(vssa_column_decoder),
        .vdd_column_driver(vdd_column_driver),
        .vdda_column_driver(vdda_column_driver),
        .vphb_bl_column_driver(vphb_bl_column_driver),
        .vphb_sl_column_driver(vphb_sl_column_driver),
        .vph_bl_column_driver(vph_bl_column_driver),
        .vph_sl_column_driver(vph_sl_column_driver),
        .vplb_bl_column_decoder(vplb_bl_column_decoder),
        .vplb_sl_column_decoder(vplb_sl_column_decoder),
        .vpl_bl_column_decoder(vpl_bl_column_decoder),
        .vpl_sl_column_decoder(vpl_sl_column_decoder),
        .precharge(precharge),
        .vpre(vpre),
        .eq(eq),
        .pchg(pchg),
        .sel_mux(sel_mux),
        .selb_mux(selb_mux),
        .vdd_sense(vdd_sense),
        .vdd_inv_sense(vdd_inv_sense),
        .vss_sense(vss_sense),
        .vth_sense(vth_sense),
        .\sense_out<0> (\sense_out<0> ),
        .\sense_out<1> (\sense_out<1> ),
        .\sense_out<2> (\sense_out<2> ),
        .\sense_out<3> (\sense_out<3> ),
        .\sense_out<4> (\sense_out<4> ),
        .\sense_out<5> (\sense_out<5> ),
        .\sense_out<6> (\sense_out<6> ),
        .\sense_out<7> (\sense_out<7> )
    );

    tran pad_w00_conn (PAD_W00, vdd_driver_wl);
    tran pad_w01_conn (PAD_W01, vss_driver_wl);
    tran pad_w02_conn (PAD_W02, vwl_p_wl_driver);
    tran pad_w03_conn (PAD_W03, vwl_n_wl_driver);
    tran pad_w04_conn (PAD_W04, vdd_decoder_wl);
    tran pad_w05_conn (PAD_W05, vdda_decoder_wl);
    tran pad_w06_conn (PAD_W06, vss_decoder_wl);
    tran pad_w07_conn (PAD_W07, vssa_decoder_wl);
    tran pad_w08_conn (PAD_W08, d0);
    tran pad_w09_conn (PAD_W09, d1);
    tran pad_w10_conn (PAD_W10, d2);
    tran pad_w11_conn (PAD_W11, d3);
    tran pad_w12_conn (PAD_W12, d4);
    tran pad_w13_conn (PAD_W13, d5);
    tran pad_w14_conn (PAD_W14, d6);
    tran pad_w15_conn (PAD_W15, d7);
    tran pad_w16_conn (PAD_W16, d8);
    tran pad_w17_conn (PAD_W17, d9);
    tran pad_w18_conn (PAD_W18, d10);
    tran pad_w19_conn (PAD_W19, d11);
    tran pad_w20_conn (PAD_W20, co);
    tran pad_w21_conn (PAD_W21, c1);
    tran pad_w22_conn (PAD_W22, c2);
    tran pad_w23_conn (PAD_W23, we);
    tran pad_w24_conn (PAD_W24, wl_in);
    tran pad_w25_conn (PAD_W25, net097);
    tran pad_w26_conn (PAD_W26, net0118);
    tran pad_w27_conn (PAD_W27, net094);
    tran pad_w28_conn (PAD_W28, net0100);
    tran pad_w29_conn (PAD_W29, net098);
    tran pad_w30_conn (PAD_W30, net099);

    tran pad_e00_conn (PAD_E00, vdd_column_decoder);
    tran pad_e01_conn (PAD_E01, vdda_column_decoder);
    tran pad_e02_conn (PAD_E02, vss_column_decoder);
    tran pad_e03_conn (PAD_E03, vssa_column_decoder);
    tran pad_e04_conn (PAD_E04, vdd_column_driver);
    tran pad_e05_conn (PAD_E05, vdda_column_driver);
    tran pad_e06_conn (PAD_E06, vphb_bl_column_driver);
    tran pad_e07_conn (PAD_E07, vphb_sl_column_driver);
    tran pad_e08_conn (PAD_E08, vph_bl_column_driver);
    tran pad_e09_conn (PAD_E09, vph_sl_column_driver);
    tran pad_e10_conn (PAD_E10, vplb_bl_column_decoder);
    tran pad_e11_conn (PAD_E11, vplb_sl_column_decoder);
    tran pad_e12_conn (PAD_E12, vpl_bl_column_decoder);
    tran pad_e13_conn (PAD_E13, vpl_sl_column_decoder);
    tran pad_e14_conn (PAD_E14, precharge);
    tran pad_e15_conn (PAD_E15, vpre);
    tran pad_e16_conn (PAD_E16, eq);
    tran pad_e17_conn (PAD_E17, pchg);
    tran pad_e18_conn (PAD_E18, sel_mux);
    tran pad_e19_conn (PAD_E19, selb_mux);
    tran pad_e20_conn (PAD_E20, vdd_sense);
    tran pad_e21_conn (PAD_E21, vdd_inv_sense);
    tran pad_e22_conn (PAD_E22, vss_sense);
    tran pad_e23_conn (PAD_E23, vth_sense);
    tran pad_e24_conn (PAD_E24, \sense_out<0> );
    tran pad_e25_conn (PAD_E25, \sense_out<1> );
    tran pad_e26_conn (PAD_E26, \sense_out<2> );
    tran pad_e27_conn (PAD_E27, \sense_out<3> );
    tran pad_e28_conn (PAD_E28, \sense_out<4> );
    tran pad_e29_conn (PAD_E29, \sense_out<5> );
    tran pad_e30_conn (PAD_E30, \sense_out<6> );
    tran pad_e31_conn (PAD_E31, \sense_out<7> );
endmodule
