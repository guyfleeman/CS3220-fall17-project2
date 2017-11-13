`timescale 1ns/1ps

`include "Processor.v"
`include "SCProc-Controller.v"

module Processor_tb;

parameter DBITS = 32;

reg clk, reset;
wire [DBITS-1:0] instr_word;

wire [3:0] proc_key_in;
wire [9:0] proc_sw_in;
wire [15:0] proc_hex_out;
wire [9:0] proc_ledr_out;
Processor #(
    .DBITS (DBITS),
    .IMEM_INIT_FILE ("test.mif")
    ) processor (
    .clk (clk),
    .reset (reset),
    .inst_word_out (instr_word),

    .key_in (proc_key_in),
    .sw_in (proc_sw_in),
    .hex_out (proc_hex_out),
    .ledr_out (proc_ledr_out)
);

wire [9:0] SW;
wire [3:0] KEY;
wire [9:0] LEDR;
wire [6:0] HEX0;
wire [6:0] HEX1;
wire [6:0] HEX2;
wire [6:0] HEX3;
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

initial begin
    $readmemh("../../assembly-files/test.hex", processor.instMem.data);
    $dumpfile("Processor.vcd");
    $dumpvars(0, Processor_tb);


    $display("      PC         R0         R1         R2         R3         ",
        "R4         R5         R6         R7         R8         R9");
    $monitor("%h", processor.pc_out[31:2],
        processor.regs.REGS[0].regs.data_out,
        processor.regs.REGS[1].regs.data_out,
        processor.regs.REGS[2].regs.data_out,
        processor.regs.REGS[3].regs.data_out,
        processor.regs.REGS[4].regs.data_out,
        processor.regs.REGS[5].regs.data_out,
        processor.regs.REGS[6].regs.data_out,
        processor.regs.REGS[7].regs.data_out,
        processor.regs.REGS[8].regs.data_out,
        processor.regs.REGS[9].regs.data_out,
        // processor.regs.REGS[10].regs.data_out,
        // processor.regs.REGS[11].regs.data_out,
        // processor.regs.REGS[12].regs.data_out,
        // processor.regs.REGS[13].regs.data_out,
        // processor.regs.REGS[14].regs.data_out,
        // processor.regs.REGS[15].regs.data_out,
        );

    // $monitor("t=%3d x=%d,y=%d,z=%d \n",$time,x,y,z, );
end

initial begin
    reset <= 0;
    clk <= 0;
    @(posedge clk);
    reset <= 1;
    @(posedge clk);
    reset <= 0;
    @(posedge clk);

    @(instr_word == 32'h0000DEAD);
    @(posedge clk);
    @(posedge clk);
    $finish;

    // @(posedge clk);
    // @(posedge clk);
    // @(posedge clk);
    // @(posedge clk);
    // @(posedge clk);
    // @(posedge clk);
    // @(posedge clk);
    // @(posedge clk);
    // @(posedge clk);
    // @(posedge clk);
    // @(posedge clk);
    // @(posedge clk);
    // @(posedge clk);
    // @(posedge clk);
    // @(posedge clk);
    // @(posedge clk);

    $finish;
end

always #10 clk = ~clk;

endmodule