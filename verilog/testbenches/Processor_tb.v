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