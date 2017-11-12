`timescale 1ns/1ps

`include "Register.v"

module Register_tb;

reg clock;
reg reset;
reg en_write;
reg [31:0] data_in;
wire [31:0] data_out;

Register #(
    .BIT_WIDTH(32),
    .RESET_VALUE(0)
    ) regs (
    .clk (clock),
    .reset (reset),
    .en_write (en_write),
    .data_in (data_in),
    .data_out (data_out)
    );

// integer i;
initial begin
    $dumpfile("Register.vcd");
    $dumpvars(0, Register_tb);
end

initial begin
    reset <= 0;
    clock <= 0;
    @(posedge clock);
    reset <= 1;
    @(posedge clock);
    reset <= 0;
    @(posedge clock);

    data_in <= 0;
    en_write <= 0;
    @(posedge clock);
    en_write <= 1;

    @(posedge clock);

    // @(posedge clock);
    // @(posedge clock);
    // @(posedge clock);


    data_in <= 9;
    @(posedge clock);
    @(posedge clock);
    @(posedge clock);

    data_in <= 7;
    @(posedge clock);
    @(posedge clock);
    // en_write = 0;
    data_in <= 8;
    @(posedge clock);
    @(posedge clock);


    $finish;
end

// Create clock
always #1 clock = ~clock;
// initial begin
//     forever begin
//     clock = 0;
//     #5 clock = ~clock;
//     end
// end

endmodule