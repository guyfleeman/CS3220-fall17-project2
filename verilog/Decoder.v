module Decoder(
input clk, reset,
input [DATA_BIT_WIDTH-1:0] data,
output reg [4:0] aluFN,
output reg [REG_INDEX_WIDTH-1:0] src_reg1, src_reg2, dest_reg,
output reg [IMM_BIT_WIDTH-1:0] imm,
output reg [1:0] aluSrc2Sel,
output reg wr_en
);

localparam REG_INDEX_WIDTH = 4;
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

always @(*) begin
    src_reg1 <= data[7:4];
    src_reg2 <= data[11:8];
    dest_reg <= data[3:0];
    imm <= data[23:8];
    wr_en = 1'b1;
end

always @(*) begin
    case (opcode)
        OP1_ALUR: begin
            aluFN <= {1'b0, fn};
            aluSrc2Sel <= 2'b00;
        end
        OP1_ALUI: begin
            aluFN <= {1'b0, fn};
            aluSrc2Sel <= 2'b01;
        end
        OP1_CMPR: begin
            aluFN <= {1'b1, fn};
            aluSrc2Sel <= 2'b00;
        end
        OP1_CMPI: begin
            aluFN <= {1'b1, fn};
            aluSrc2Sel <= 2'b01;
        end
        default: begin
            aluFN <= 5'bzzzzz;
            aluSrc2Sel <= 2'bzz;
        end
    endcase
end

endmodule