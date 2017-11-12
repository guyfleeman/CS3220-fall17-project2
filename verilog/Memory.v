module Memory (
input clk, reset, en_write,
input [ADDR_BIT_WIDTH - 1 : 0] addr,
input [DATA_BIT_WIDTH - 1 : 0] data_in,
output [DATA_BIT_WIDTH - 1 : 0] data_out
);

parameter MEM_INIT_FILE = "";
parameter ADDR_BIT_WIDTH = 11;
parameter DATA_BIT_WIDTH = 32;

localparam SIZE = (1 << ADDR_BIT_WIDTH);

(* ram_init_file = MEM_INIT_FILE *)

reg[DATA_BIT_WIDTH - 1 : 0] data[0 : SIZE - 1];

assign data_out = data[addr];

always @(posedge clk) begin
    if (en_write)
        data[addr] <= data_in;
end

endmodule