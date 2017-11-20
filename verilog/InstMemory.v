`ifndef _INST_MEMORY_
`define _INST_MEMORY_

module InstMemory(
input clk,
input[ADDR_BIT_WIDTH - 1: 0] addr,
output reg[DATA_BIT_WIDTH - 1: 0] dataOut
);

parameter MEM_INIT_FILE = "";
parameter ADDR_BIT_WIDTH = 11;
parameter DATA_BIT_WIDTH = 32;
parameter N_WORDS = (1 << ADDR_BIT_WIDTH);

(* ram_init_file = MEM_INIT_FILE *)
reg[DATA_BIT_WIDTH - 1: 0] data[0: N_WORDS - 1];

always @(negedge clk) begin
	dataOut <= data[addr];
end

endmodule

`endif //_INST_MEMORY_