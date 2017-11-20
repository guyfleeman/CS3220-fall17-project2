`include "Processor.v"
`include "SCProc-Controller.v"

module Project2(
input  [9:0] SW,
input  [3:0] KEY,
input  CLOCK_50,
input  FPGA_RESET_N,
output [9:0] LEDR,
output [6:0] HEX0,
output [6:0] HEX1,
output [6:0] HEX2,
output [6:0] HEX3
);
parameter DBITS                 = 32;
parameter IMEM_INIT_FILE        = "test.mif";

parameter DMEM_ADDR_BIT_WIDTH   = 11;
parameter IMEM_ADDR_BIT_WIDTH   = 11;


//PLL, clock generation, and reset generation
wire clk, lock;
//Pll pll(.inclk0(CLOCK_50), .c0(clk), .locked(lock));
PLL	PLL_inst (
    .refclk (CLOCK_50),
    .rst(!FPGA_RESET_N),
    .outclk_0 (clk),
    .locked (lock)
);

wire reset = ~lock;

wire [15:0] proc_hex_out;
Processor #(
    .DBITS (DBITS),
    .IMEM_INIT_FILE (IMEM_INIT_FILE)
    ) processor (
    .clk (clk),
    .reset (reset),

    .key_in (KEY),
    .sw_in (SW),
    .hex_out (proc_hex_out),
    .ledr_out (LEDR)
);

SevenSeg sseg0 (.dIn (proc_hex_out[3:0]),   .dOut (HEX0));
SevenSeg sseg1 (.dIn (proc_hex_out[7:4]),   .dOut (HEX1));
SevenSeg sseg2 (.dIn (proc_hex_out[11:8]),  .dOut (HEX2));
SevenSeg sseg3 (.dIn (proc_hex_out[15:12]), .dOut (HEX3));

endmodule
