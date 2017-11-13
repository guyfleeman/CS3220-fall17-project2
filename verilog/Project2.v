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
parameter IMEM_INIT_FILE        = "Sorter2.mif";

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

wire [3:0] proc_key_in;
wire [9:0] proc_sw_in;
wire [15:0] proc_hex_out;
wire [9:0] proc_ledr_out;
Processor #(
    .DBITS (DBITS),
    .IMEM_INIT_FILE (IMEM_INIT_FILE)
    ) processor (
    .clk (clk),
    .reset (reset),

    .key_in (proc_key_in),
    .sw_in (proc_sw_in),
    .hex_out (proc_hex_out),
    .ledr_out (proc_ledr_out)
);


SCProcController controller (
    .key_in (KEY),
    .ledr_in (proc_ledr_out),
    .key_out (proc_key_in),
    .ledr_out (LEDR),

    .sw_in (SW),
    .sw_out (proc_sw_in),

    .hex_in (proc_hex_out),
    .hex0_out (HEX0),
    .hex1_out (HEX1),
    .hex2_out (HEX2),
    .hex3_out (HEX3)
);

endmodule
