`timescale 1ns/1ps

module RegisterFile_tb;

reg clk;
reg reset;
reg en_write;
reg [3:0] sr1_ind, sr2_ind, dr_ind;
reg [31:0] data_in;
wire [31:0] sr1, sr2;

RegisterFile #(
    .BIT_WIDTH(32),
    .RESET_VALUE(0),
    .REG_INDEX_WIDTH(4)
    ) reg_file (
    .clk (clk),
    .reset (reset),
    .en_write (en_write),
    .sr1_ind (sr1_ind),
    .sr2_ind (sr2_ind),
    .dr_ind (dr_ind),
    .data_in (data_in),
    .sr1 (sr1),
    .sr2 (sr2)
);

// integer i;
initial begin
    $dumpfile("RegisterFile.vcd");
    $dumpvars(0, RegisterFile_tb);

    reset <= 0;
    clk <= 0;
    @(posedge clk);
    reset <= 1;
    @(posedge clk);
    reset <= 0;
    @(posedge clk);

    sr1_ind <= 0;
    sr2_ind <= 0;
    data_in <= 0;
    dr_ind <= 0;
    @(posedge clk);

    sr1_ind <= 1;
    sr2_ind <= 2;
    @(posedge clk);
    $display("1) Expected: [sr1,sr2]=[0,0], got: [%d,%d]", sr1, sr2);

    dr_ind <= 1;
    en_write <= 1;
    data_in <= 9;
    @(posedge clk);
    en_write <= 0;
    $display("1) Expected: [sr1,sr2]=[9,0], got: [%d,%d]", sr1, sr2);
    @(posedge clk);

    data_in <= 10;
    @(posedge clk);
    $display("1) Expected: [sr1,sr2]=[9,0], got: [%d,%d]", sr1, sr2);
    en_write <= 1;
    data_in <= 7;
    @(posedge clk);
    $display("1) Expected: [sr1,sr2]=[9,0], got: [%d,%d]", sr1, sr2);
    data_in <= 8;
    @(posedge clk);
    en_write <= 0;
    $display("1) Expected: [sr1,sr2]=[7,0], got: [%d,%d]", sr1, sr2);
    @(posedge clk);
    $display("1) Expected: [sr1,sr2]=[7,0], got: [%d,%d]", sr1, sr2);


    $finish;
end

// Create clock
always #2 clk = ~clk;

endmodule