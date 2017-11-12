`timescale 1ns/1ps

module Processor_tb;

reg clk, reset;

Processor #(
    .DBITS (32),
    .IMEM_INIT_FILE ("test.mif")
    ) processor (
    .clk (clk),
    .reset (reset)
);

initial begin
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

    @(posedge clk);
    @(posedge clk);
    @(posedge clk);
    @(posedge clk);
    @(posedge clk);
    $finish;
end

always #10 clk = ~clk;

endmodule