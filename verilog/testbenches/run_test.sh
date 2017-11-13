#!/bin/bash

if [ ! -f $1 ]; then
    echo "File not found"
    exit 1
fi

if [ "$(basename "$1")" == "Processor_tb.v" ]; then
    python ../../assembler.py ../../assembly-files/test.a32
fi

out_name="$(basename "$1"  _tb.v)"
iverilog -o $out_name -I ../ -I ../../assembly-files/ $1 && vvp $out_name