module Alu(
input clk, reset,
input [4:0] aluOP,
input [BIT_WIDTH-1:0] in1, in2,
output reg [BIT_WIDTH-1:0] out
);

parameter BIT_WIDTH = 32;

localparam ADD  = 5'b00011;
localparam SUB  = 5'b00010;
localparam AND  = 5'b00111;
localparam OR   = 5'b00110;
localparam XOR  = 5'b00101;
localparam NAND = 5'b01011;
localparam NOR  = 5'b01010;
localparam XNOR = 5'b01001;

localparam F   = 5'b10011;
localparam EQ  = 5'b11100;
localparam LT  = 5'b11101;
localparam LTE = 5'b10010;
localparam T   = 5'b11111;
localparam NE  = 5'b10000;
localparam GTE = 5'b10001;
localparam GT  = 5'b11110;

always @(posedge clk) begin
    case (aluOP)
        ADD  : out <= in1 + in2;
        SUB  : out <= in1 - in2;
        AND  : out <= in1 & in2;
        OR   : out <= in1 | in2;
        XOR  : out <= in1 ^ in2;
        NAND : out <= in1 ~& in2;
        NOR  : out <= in1 ~| in2;
        XNOR : out <= in1 ~^ in2;

        F    : out <= 0;
        EQ   : out <= (in1 == in2) ? 1 : 0;
        LT   : out <= (in1 < in2) ? 1 : 0;
        LTE  : out <= (in1 <= in2) ? 1 : 0;
        T    : out <= 1;
        NE   : out <= (in1 != in2) ? 1 : 0;
        GTE  : out <= (in1 >= in2) ? 1 : 0;
        GT   : out <= (in1 > in2) ? 1 : 0;
        default : out <= 0;
    endcase
end

endmodule