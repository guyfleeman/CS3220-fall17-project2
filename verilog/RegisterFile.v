`ifndef _REGISTER_FILE_
`define _REGISTER_FILE_

`include "Register.v"

module RegisterFile(
input clk, reset, en_write,
input [REG_INDEX_WIDTH-1:0] sr1_ind, sr2_ind, dr_ind,
input [BIT_WIDTH-1:0] data_in,
output [BIT_WIDTH-1:0] sr1, sr2
);

parameter BIT_WIDTH = 32;
parameter REG_INDEX_WIDTH = 4;
parameter RESET_VALUE = 0;

wire [BIT_WIDTH-1:0] reg_data_out [(1<<REG_INDEX_WIDTH)-1:0];

genvar i;
generate
    for (i=0; i<(1<<REG_INDEX_WIDTH); i=i+1) begin : REGS
        wire en_write1;
        Register #(
            .BIT_WIDTH(BIT_WIDTH), .RESET_VALUE(RESET_VALUE)
            ) regs (
            .clk (clk),
            .reset (reset),
            .en_write (en_write1),
            .data_in (data_in),
            .data_out (reg_data_out[i])
            );
        assign en_write1 = (dr_ind == i) ? en_write : 0;
        // initial begin
        //     $monitor("%d\t", regs.data_out);
        // end
    end
endgenerate


assign sr1 = reg_data_out[sr1_ind];
assign sr2 = reg_data_out[sr2_ind];

endmodule

`endif //_REGISTER_FILE_