// Black-box interface templates for the 3D_TFT GDS cells.
//
// These are OpenLane integration placeholders, not extracted electrical
// netlists. The available GDS files do not contain pin labels, so verify
// every port list against schematic/CDL/SPICE before signoff.

`ifndef _3D_TFT_BLACKBOXES_V_
`define _3D_TFT_BLACKBOXES_V_

(* blackbox *)
module nfet_W20p825_L5 (
`ifdef USE_POWER_PINS
    inout VSS,
`endif
    inout D,
    input G,
    inout S
);
endmodule

(* blackbox *)
module nfet_W24u_L5 (
`ifdef USE_POWER_PINS
    inout VSS,
`endif
    inout D,
    input G,
    inout S
);
endmodule

(* blackbox *)
module nfet_W6u_L5 (
`ifdef USE_POWER_PINS
    inout VSS,
`endif
    inout D,
    input G,
    inout S
);
endmodule

(* blackbox *)
module INV_X4PC_T5_nmos (
`ifdef USE_POWER_PINS
    inout VDD,
    inout VSS,
`endif
    input A,
    output Y
);
endmodule

(* blackbox *)
module wl_inv (
`ifdef USE_POWER_PINS
    inout VDD,
    inout VSS,
`endif
    input A,
    output Y
);
endmodule

(* blackbox *)
module wl_prebuffer (
`ifdef USE_POWER_PINS
    inout VDD,
    inout VSS,
`endif
    input A,
    output Y
);
endmodule

(* blackbox *)
module wl_sel (
`ifdef USE_POWER_PINS
    inout VDD,
    inout VSS,
`endif
    input A,
    input SEL,
    output Y
);
endmodule

(* blackbox *)
module stack_sram_array_f0;
endmodule

(* blackbox *)
module stack_sram_array_f1;
endmodule

(* blackbox *)
module stack_sram_array_f2;
endmodule

(* blackbox *)
module stack_sram_array_f3;
endmodule

(* blackbox *)
module stack_sram_array_f4;
endmodule

(* blackbox *)
module stack_sram_array_f5;
endmodule

`endif
