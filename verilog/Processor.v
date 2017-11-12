module Processor (
input clk,
input reset,
output [IMEM_DATA_BIT_WIDTH - 1: 0] inst_word_out // For testing
);

parameter DBITS                 = 32;
parameter IMEM_INIT_FILE        = "Sorter2.mif";

localparam INST_SIZE             = 32'd4;
localparam INST_BIT_WIDTH        = 32;
localparam START_PC              = 32'h40;
localparam REG_INDEX_BIT_WIDTH   = 4;

localparam IMEM_ADDR_BIT_WIDTH   = 11;
localparam IMEM_DATA_BIT_WIDTH   = INST_BIT_WIDTH;
localparam IMEM_PC_BITS_HI       = IMEM_ADDR_BIT_WIDTH + 2;
localparam IMEM_PC_BITS_LO       = 2;

// Create PC and its logic
wire pcWrtEn = 1'b1;
reg [DBITS - 1: 0] pcIn;
wire [DBITS - 1: 0] pcOut;

Register #(
    .BIT_WIDTH(DBITS), .RESET_VALUE(START_PC)
    ) pc (
    clk, reset, pcWrtEn, pcIn, pcOut
);

always @(*) begin
    if (instWord == 32'h0000DEAD) begin
        pcIn <= pcOut;
        // $finish;
    end else begin
        pcIn <= pcOut + 4;
    end
end

assign inst_word_out = instWord;

// assign pcIn = (instWord != 32'h0000DEAD) ? pcOut + 4 : pcOut;

wire [IMEM_DATA_BIT_WIDTH - 1: 0] instWord;
InstMemory #(
    IMEM_INIT_FILE,
    IMEM_ADDR_BIT_WIDTH,
    IMEM_DATA_BIT_WIDTH
    ) instMem (
    .addr (pcOut[IMEM_PC_BITS_HI - 1: IMEM_PC_BITS_LO]),
    .dataOut (instWord)
);

wire [4:0] aluFN;
wire [3:0] src_reg1, src_reg2, dest_reg;
wire [15:0] imm;
wire [1:0] aluSrc2Sel;
wire wr_en;
Decoder decoder (
    .clk (clk),
    .reset (reset),
    .data (instWord),
    .aluFN (aluFN),
    .src_reg1 (src_reg1),
    .src_reg2 (src_reg2),
    .dest_reg (dest_reg),
    .imm (imm),
    .aluSrc2Sel (aluSrc2Sel),
    .wr_en (wr_en)
);

wire [DBITS-1:0] alu_out, regs_out1, regs_out2;
wire reg_write;

assign reg_write = 1'b1;

RegisterFile #(
    .BIT_WIDTH (DBITS),
    .REG_INDEX_WIDTH (REG_INDEX_BIT_WIDTH),
    .RESET_VALUE (0)
    ) regs (
    .clk (clk),
    .reset (reset),
    .en_write (reg_write),
    .sr1_ind (src_reg1),
    .sr2_ind (src_reg2),
    .dr_ind (dest_reg),
    .data_in (alu_out),
    .sr1 (regs_out1),
    .sr2 (regs_out2)
);

wire [DBITS-1:0] imm_ext;
SignExtension #(
    .IN_BIT_WIDTH (16),
    .OUT_BIT_WIDTH (DBITS)
    ) sign_extend (
    .dIn (imm),
    .dOut (imm_ext)
);

wire [DBITS-1:0] alu_in2;
Mux4to1 #(
    .BIT_WIDTH (DBITS)
    ) alu_in2_mux (
    .clk (clk),
    .reset (reset),
    .select (aluSrc2Sel),
    .in0 (regs_out2),
    .in1 (imm_ext),
    .in2 (32'hzzzzzzzz),
    .in3 (32'hzzzzzzzz),
    .out (alu_in2)
);

Alu #(
    .BIT_WIDTH (DBITS)
    ) alu (
    .clk (clk),
    .reset (reset),
    .aluFN (aluFN),
    .in1 (regs_out1),
    .in2 (alu_in2),
    .out (alu_out)
);

endmodule