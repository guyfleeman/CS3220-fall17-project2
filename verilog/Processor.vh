`ifndef _DECODER_VH_
`define _DECODER_VH_

`define OP_ALUR     4'b1111
`define OP_ALUI     4'b1011
`define OP_CMPR     4'b1110
`define OP_CMPI     4'b1010
`define OP_BCOND    4'b0000
`define OP_SW       4'b1000
`define OP_LW       4'b1001
`define OP_JAL      4'b0001

`define FN_ADD      5'b00011
`define FN_SUB      5'b00010
`define FN_AND      5'b00111
`define FN_OR       5'b00110
`define FN_XOR      5'b00101
`define FN_NAND     5'b01011
`define FN_NOR      5'b01010
`define FN_XNOR     5'b01001

`define FN_F        5'b10011
`define FN_EQ       5'b11100
`define FN_LT       5'b11101
`define FN_LTE      5'b10010
`define FN_T        5'b11111
`define FN_NE       5'b10000
`define FN_GTE      5'b10001
`define FN_GT       5'b11110

`define ALU_SRC2_REG2   2'b00
`define ALU_SRC2_IMM    2'b01
`define ALU_SRC2_IMM4   2'b10
`define ALU_SRC2_ZERO   2'b11

`define REG_IN_PC4      2'b00
`define REG_IN_DOUT     2'b01
`define REG_IN_ALU      2'b10

`define PC_IN_IMM4      2'b00
`define PC_IN_ALU       2'b01
`define PC_IN_PC4       2'b10
`define PC_IN_PC        2'b11

`define DEAD            16'hDEAD

`endif