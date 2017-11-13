`timescale 1ns/1ps

`include "Processor.v"

module Processor_tb;

parameter DBITS = 32;

reg clk, reset;
wire [DBITS-1:0] instr_word;

Processor #(
    .DBITS (DBITS),
    .IMEM_INIT_FILE ("test.mif")
    ) processor (
    .clk (clk),
    .reset (reset),
    .inst_word_out (instr_word)
);

initial begin
    $readmemh("../../assembly-files/test.hex", processor.instMem.data);
    $dumpfile("Processor.vcd");
    $dumpvars(0, Processor_tb);


    $display("      PC        R0        R1        R2        R3        ",
        "R4        R5        R6        R7        R8        R9");
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