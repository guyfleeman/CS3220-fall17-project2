`include "Alu.v"
`include "Decoder.v"
`include "InstMemory.v"
`include "Mux4to1.v"
`include "Register.v"
`include "RegisterFile.v"
`include "SignExtension.v"
`include "Memory.v"

module Processor (
input clk,
input reset,
output [INST_BIT_WIDTH - 1: 0] inst_word_out // For testing
);

parameter DBITS                 = 32;
parameter IMEM_INIT_FILE        = "Sorter2.mif";
parameter DMEM_INIT_FILE        = "";

parameter DMEM_ADDR_BIT_WIDTH   = 11;
parameter IMEM_ADDR_BIT_WIDTH   = 11;

localparam INST_SIZE            = 32'd4;
localparam INST_BIT_WIDTH       = 32;
localparam START_PC             = 32'h40;
localparam REG_INDEX_BIT_WIDTH  = 4;
localparam IMEM_WORD_BITS       = 2;
localparam DMEM_WORD_BITS       = 2;


wire [DBITS-1:0] alu_out;
reg [DBITS-1:0] alu_in2;

// PC Mux
always @(*) begin
    case (sel_pc)
        `PC_IN_IMM4:    pc_in = imm_ext4 + pc_out + 4;
        `PC_IN_ALU:     pc_in = alu_out;
        `PC_IN_PC4:     pc_in = pc_out + 4;
        `PC_IN_PC:      pc_in = pc_out;
        default:        pc_in = {DBITS{1'bz}};
    endcase
end

// PC signals
reg [DBITS - 1: 0] pc_in;
wire [DBITS - 1: 0] pc_out;
wire pc_en = 1'b1;
Register #(
    .BIT_WIDTH(DBITS), .RESET_VALUE(START_PC)
    ) pc (
    clk, reset, pc_en, pc_in, pc_out
);


// Instruction memory signals
wire [INST_BIT_WIDTH - 1: 0] inst_word;
assign inst_word_out = inst_word;
InstMemory #(
    IMEM_INIT_FILE,
    IMEM_ADDR_BIT_WIDTH,
    INST_BIT_WIDTH
    ) instMem (
    .addr (pc_out[IMEM_ADDR_BIT_WIDTH + IMEM_WORD_BITS - 1: IMEM_WORD_BITS]),
    .dataOut (inst_word)
);


// Control/data signals from decoder
wire [4:0] alu_fn;
wire [3:0] src_reg1, src_reg2, dest_reg;
wire [15:0] imm;
wire [1:0] sel_pc, sel_alu_sr2, sel_reg_din;
wire wr_reg, wr_mem;
Decoder decoder (
    .data (inst_word),
    .alu_out (alu_out),
    .alu_fn (alu_fn),
    .src_reg1 (src_reg1),
    .src_reg2 (src_reg2),
    .dest_reg (dest_reg),
    .imm (imm),
    .sel_alu_sr2 (sel_alu_sr2),
    .sel_pc (sel_pc),
    .sel_reg_din (sel_reg_din),
    .wr_reg (wr_reg),
    .wr_mem (wr_mem)
);

// Register File Mux
always @(*) begin
    case (sel_reg_din)
        `REG_IN_PC4:    regs_din = pc_out + 4;
        `REG_IN_DOUT:   regs_din = data_out;
        `REG_IN_ALU:    regs_din = alu_out;
        default:        regs_din = {DBITS{1'bz}};
    endcase
end

reg [DBITS-1:0] regs_din;
wire [DBITS-1:0] regs_out1, regs_out2;
RegisterFile #(
    .BIT_WIDTH (DBITS),
    .REG_INDEX_WIDTH (REG_INDEX_BIT_WIDTH),
    .RESET_VALUE (0)
    ) regs (
    .clk (clk),
    .reset (reset),
    .en_write (wr_reg),
    .sr1_ind (src_reg1),
    .sr2_ind (src_reg2),
    .dr_ind (dest_reg),
    .data_in (regs_din),
    .sr1 (regs_out1),
    .sr2 (regs_out2)
);


// Sign extended signals
wire [DBITS-1:0] imm_ext;
wire [DBITS-1:0] imm_ext4 = {imm_ext[DBITS-3:0], 2'b00};
SignExtension #(
    .IN_BIT_WIDTH (16),
    .OUT_BIT_WIDTH (DBITS)
    ) sign_extend (
    .dIn (imm),
    .dOut (imm_ext)
);


// ALU input 2 Mux
always @(*) begin
    case (sel_alu_sr2)
        `ALU_SRC2_REG2:     alu_in2 = regs_out2;
        `ALU_SRC2_IMM:      alu_in2 = imm_ext;
        `ALU_SRC2_IMM4:     alu_in2 = imm_ext4;
        `ALU_SRC2_ZERO:     alu_in2 = 0;
        default:            alu_in2 = {DBITS{1'bz}};
    endcase
end

// ALU signals
Alu #(
    .BIT_WIDTH (DBITS)
    ) alu (
    .alu_fn (alu_fn),
    .in1 (regs_out1),
    .in2 (alu_in2),
    .out (alu_out)
);



wire [DBITS-1:0] data_out;
Memory #(
    .MEM_INIT_FILE (DMEM_INIT_FILE),
    .ADDR_BIT_WIDTH (DMEM_ADDR_BIT_WIDTH),
    .DATA_BIT_WIDTH (DBITS)
    ) data_memory (
    .clk (clk),
    .reset (reset),
    .en_write (wr_mem),
    .addr (alu_out[DMEM_ADDR_BIT_WIDTH + DMEM_WORD_BITS - 1: DMEM_WORD_BITS]),
    .data_in (regs_out2),
    .data_out (data_out)
);


endmodule