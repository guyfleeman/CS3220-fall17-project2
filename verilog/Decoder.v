module Decoder(
input clk, reset,
input [DATA_BIT_WIDTH-1:0] data,
output reg [4:0] aluOP,
output reg [REG_INDEX_WIDTH-1:0] src_reg1, src_reg2, dest_reg,
output reg [IMM_BIT_WIDTH-1:0] imm,
output reg [2:0] aluSrc2Sel
);

parameter REG_INDEX_WIDTH = 4;

localparam DATA_BIT_WIDTH = 32;
localparam IMM_BIT_WIDTH = 16;

localparam OP1_ALUR  = 4'b1111;
localparam OP1_ALUI  = 4'b1011;
localparam OP1_CMPR  = 4'b1110;
localparam OP1_CMPI  = 4'b1010;
// localparam OP1_BCOND = 4'b0000;
// localparam OP1_SW    = 4'b1001;
// localparam OP1_LW    = 4'b1000;
// localparam OP1_JAL   = 4'b0001;

wire [3:0] fn;
wire [3:0] opcode;

assign fn = data[31:28];
assign opcode = data[27:24];

always @(clk) begin
    src_reg1 <= data[7:4];
    src_reg2 <= data[11:8];
    dest_reg <= data[3:0];
    imm <= data[23:8];
end

always @(clk) begin
    case (fn)
        OP1_ALUR: begin
            aluOP <= {1'b0, opcode};
            aluSrc2Sel <= 2'b00;
        end
        OP1_ALUI: begin
            aluOP <= {1'b0, opcode};
            aluSrc2Sel <= 2'b01;
        end
        OP1_CMPR: begin
            aluOP <= {1'b1, opcode};
            aluSrc2Sel <= 2'b00;
        end
        OP1_CMPI: begin
            aluOP <= {1'b1, opcode};
            aluSrc2Sel <= 2'b01;
        end
    endcase
end

endmodule