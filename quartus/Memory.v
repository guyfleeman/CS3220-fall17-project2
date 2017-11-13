`ifndef _MEMORY_
`define _MEMORY_

`include "Processor.vh"

module Memory (
input clk, reset, en_write,
input [29 : 0] addr,
input [DATA_BIT_WIDTH - 1: 0] data_in,
output reg [DATA_BIT_WIDTH - 1 : 0] data_out,

input [3:0] mmio_key_in,
input [9:0] mmio_sw_in,
output [15:0] mmio_hex_out,
output [9:0] mmio_ledr_out
);

parameter MEM_INIT_FILE = "";
parameter ADDR_BIT_WIDTH = 11;
parameter DATA_BIT_WIDTH = 32;

localparam SIZE = (1 << ADDR_BIT_WIDTH);

(* ram_init_file = MEM_INIT_FILE *)

reg [DATA_BIT_WIDTH - 1 : 0] data [0 : SIZE - 1];
reg [15:0] mmio_hex;
reg [9:0] mmio_ledr;
reg [3:0] mmio_key;
reg [9:0] mmio_sw;

assign mmio_hex_out = mmio_hex;
assign mmio_ledr_out = mmio_ledr;

always @(*) begin
    if (addr < 1 << ADDR_BIT_WIDTH)
        data_out = data[addr];
    else begin
        case (addr)
            `ADDR_HEX: data_out = {16'b0, mmio_hex};
            `ADDR_LEDR: data_out = {22'b0, mmio_ledr};
            `ADDR_KEY: data_out = {28'b0, mmio_key};
            `ADDR_SW: data_out = {22'b0, mmio_sw};
            default: data_out = 32'hzzzzzzzz;
        endcase
    end
end

always @(posedge clk) begin
    mmio_key <= mmio_key_in;
    mmio_sw <= mmio_sw_in;
end

always @(posedge clk) begin
    if (en_write) begin
        case (addr)
            `ADDR_HEX:  mmio_hex <= data_in[15:0];
            `ADDR_LEDR: mmio_ledr <= data_in[9:0];
            default:    data[addr] <= data_in[ADDR_BIT_WIDTH-1:0];
        endcase
    end
end

endmodule

`endif //_MEMORY_