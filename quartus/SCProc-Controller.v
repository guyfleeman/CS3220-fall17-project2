`ifndef _SC_PROC_CONTROLLER_
`define _SC_PROC_CONTROLLER_

`include "SevenSeg.v"

module SCProcController (
input [3:0] key_in,
input [9:0] ledr_in,
output [3:0] key_out,
output [9:0] ledr_out,

input [9:0] sw_in,
output [9:0] sw_out,

input [15:0] hex_in,
output [6:0] hex0_out,
output [6:0] hex1_out,
output [6:0] hex2_out,
output [6:0] hex3_out
);

assign key_out = key_in;
assign ledr_out = ledr_in;
assign sw_out = sw_in;

SevenSeg sseg0 (.dIn (hex_in[3:0]),   .dOut (hex0_out));
SevenSeg sseg1 (.dIn (hex_in[7:4]),   .dOut (hex1_out));
SevenSeg sseg2 (.dIn (hex_in[11:8]),  .dOut (hex2_out));
SevenSeg sseg3 (.dIn (hex_in[15:12]), .dOut (hex3_out));

endmodule

`endif //_SC_PROC_CONTROLLER_