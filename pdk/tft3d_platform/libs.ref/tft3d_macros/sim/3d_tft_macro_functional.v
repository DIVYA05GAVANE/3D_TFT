// Functional Verilog models for imported 3D_TFT macros.
// These are for digital simulation only; layout integration uses black boxes.

module nfet_W20p825_L5 (inout D, input G, inout S);
endmodule

module nfet_W24u_L5 (inout D, input G, inout S);
endmodule

module nfet_W6u_L5 (inout D, input G, inout S);
endmodule

module INV_X4PC_T5_nmos (input A, output Y);
    assign Y = ~A;
endmodule

module wl_inv (input A, output Y);
    assign Y = ~A;
endmodule

module wl_prebuffer (input A, output Y);
    assign Y = A;
endmodule

module wl_sel (input A, input SEL, output Y);
    assign Y = SEL ? A : 1'b1;
endmodule

// Physical-only SRAM array flavour placeholders. The source GDS has no named
// electrical pins, so these modules intentionally have no ports.
module stack_sram_array_f0;
endmodule

module stack_sram_array_f1;
endmodule

module stack_sram_array_f2;
endmodule

module stack_sram_array_f3;
endmodule

module stack_sram_array_f4;
endmodule

module stack_sram_array_f5;
endmodule
