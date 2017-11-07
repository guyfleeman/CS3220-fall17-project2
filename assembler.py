#!/usr/bin/python

import sys
import os


if len(sys.argv) < 2:
    print("No file provided")
    exit(1)

nameout = os.path.splitext(sys.argv[1])[0] + ".mif"
if len(sys.argv) >= 3:
    nameout = sys.argv[2]

fout = open(nameout, "w")

lines = []
labels = {}

def getDecimal(numIn):
    out = 0
    if numIn.lower().startswith("0x"):
        out = int(numIn[2:], 16)
    else:
        out = int(numIn)
    if (out < 0):
        out = -(-out - (1<<16))
    return out

with open(sys.argv[1]) as f:
    lastAddr = 0
    currAddr = 0
    for line in f:
        line = line.replace("\n","")
        label = ""
        if (line == ""):
            continue

        l1 = line.split(":", 1)
        if (len(l1) == 2):
            line = l1[1]
            label = l1[0]


        if (line != ""):
            line = line.split(None, 1)
            line = line[0:-1] + line[-1].split(",")
            line = [i.strip() for i in line]

        labelAddr = currAddr
        lineNext = ""

        if (len(line) == 2 and line[0].lower() == ".orig"):
            # handle .orig
            currAddr = getDecimal(line[1])/4
            lastAddr = currAddr
            line = ""
        elif (len(line) == 2 and line[0].lower() == '.name'):
            # handle .name
            label, labelAddrTemp = line[1].split("=");
            labelAddr = getDecimal(labelAddrTemp)/4
            line = ""
        elif (line != ""):
            # psuedo instructions
            if (line[0].lower() == "br"):
                line = ["BEQ", line[1], "R6", "R6"]
            elif (line[0].lower() == "not"):
                line = ["NAND", line[1], line[1], line[2]]
            elif (line[0].lower() == "ble"):
                line = ["LTE", line[2], line[3], "R6"]
                lineNext = ["BNEZ", line[1], "R6"]
            elif (line[0].lower() == "bge"):
                line = ["GTE", line[2], line[3], "R6"]
                lineNext = ["BNEZ", line[1], "R6"]
            elif (line[0].lower() == "call"):
                line = ["JAL", line[1], "RA"]
            elif (line[0].lower() == "ret"):
                line = ["JAL", "0(RA)", "R9"]
            elif (line[0].lower() == "jmp"):
                line = ["JAL", line[1], "R9"]

        label = label.lower()
        if label != "" :
            labels[label] = labelAddr

        if (line != ""):
            lines.append([currAddr] + line)
            currAddr += 1
            if (lineNext != ""):
                lines.append([currAddr] + line)
                currAddr += 1

# print lines
# print labels

opcodes = {
    "ADD"   : "1111 0011",
    "SUB"   : "1111 0010",
    "AND"   : "1111 0111",
    "OR"    : "1111 0110",
    "XOR"   : "1111 0101",
    "NAND"  : "1111 1011",
    "NOR"   : "1111 1010",
    "XNOR"  : "1111 1001",

    "ADDI"  : "1011 0011",
    "SUBI"  : "1011 1011",
    "ANDI"  : "1011 0111",
    "ORI"   : "1011 0110",
    "XORI"  : "1011 0101",
    "NANDI" : "1011 1011",
    "NORI"  : "1011 1010",
    "XNORI" : "1011 1001",
    "MVHI"  : "1011 1001",

    "LW"    : "1000 0000",
    "SW"    : "1001 0000",

    "F"     : "1110 0011",
    "EQ"    : "1110 1100",
    "LT"    : "1110 1101",
    "LTE"   : "1110 0010",
    "T"     : "1110 1111",
    "NE"    : "1110 0000",
    "GTE"   : "1110 0001",
    "GT"    : "1110 1110",

    "FI"    : "1010 0011",
    "EQI"   : "1010 1100",
    "LTI"   : "1010 1101",
    "LTEI"  : "1010 0010",
    "TI"    : "1010 1111",
    "NEI"   : "1010 0000",
    "GTEI"  : "1010 0001",
    "GTI"   : "1010 1110",

    "BF"    : "0000 0011",
    "BEQ"   : "0000 1100",
    "BLT"   : "0000 1101",
    "BLTE"  : "0000 0010",
    "BEQZ"  : "0000 1000",
    "BLTZ"  : "0000 1001",
    "BLTEZ" : "0000 0110",
    "BT"    : "0000 1111",
    "BNE"   : "0000 0000",
    "BGTE"  : "0000 0001",
    "BGT"   : "0000 1110",
    "BNEZ"  : "0000 0100",
    "BGTEZ" : "0000 0101",
    "BGTZ"  : "0000 1010",

    "JAL"   : "0001 0000"
}

registers = {"r%d" % i : i for i in range(16)}
registers['a0'] = 0;
registers['a1'] = 1;
registers['a2'] = 2;
registers['a3'] = 3;
registers['rv'] = 3;
registers['t0'] = 4;
registers['t1'] = 5;
registers['s0'] = 6;
registers['s1'] = 7;
registers['s2'] = 8;
registers['gp'] = 12;
registers['fp'] = 13;
registers['sp'] = 14;
registers['ra'] = 15;

opRRR = ['add', 'sub', 'and', 'or', 'xor', 'nand', 'nor', 'xnor', 'f', 'eq',
         'lt', 'lte', 't', 'ne', 'gte', 'gt']
opIRR = ['addi', 'subi', 'andi', 'ori', 'xori', 'nandi', 'nori', 'xnori', 'fi',
         'eqi', 'lti', 'ltei', 'ti', 'nei', 'gtei', 'gti', 'bf', 'beq', 'blt',
         'blte', 'bt', 'bne', 'bgte', 'bgt']
opIR = ['mvhi', 'beqz', 'bltz', 'bltez', 'bnez', 'bgtez', 'bgtz']
opPCRel = ['bf', 'beq', 'blt', 'blte', 'beqz', 'bltz', 'bltez', 'bt', 'bne',
           'bgte', 'bgt', 'bnez', 'bgtez', 'bgtz']

# specials: LW SW JAL

mifOut = []
mifOut += ['WIDTH=32;']
mifOut += ['DEPTH=2048;']
mifOut += ['ADDRESS_RADIX=HEX;']
mifOut += ['DATA_RADIX=HEX;']
mifOut += ['CONTENT BEGIN']

for line in lines:
    currAddr = line[0]
    instr = line[1].lower()
    if instr.lower() == ".word":
        op = ""
    else:
        op = hex(int(opcodes[instr].replace(' ', ''), 2))[2:].zfill(2)

    out = ''

    if (instr.lower() in opRRR):
        out = op + '000' + hex(registers[line[2].lower()])[2:] \
            + hex(registers[line[3].lower()])[2:] \
            + hex(registers[line[4].lower()])[2:]
    elif (instr.lower() in opIRR):
        imm = line[2]
        if (str(imm).lower() in labels):
            imm = labels[imm.lower()]*4
        out = op + hex(getDecimal(str(imm)))[2:].zfill(4) \
            + hex(registers[line[3].lower()])[2:] \
            + hex(registers[line[4].lower()])[2:]
    elif (instr.lower() in opIR):
        imm = line[2]
        if (str(imm).lower() in labels):
            imm = labels[imm.lower()]*4
        out = op + hex(getDecimal(str(imm)))[2:].zfill(4) \
            + hex(registers[line[3].lower()])[2:] + '0'
    elif (instr.lower() == 'lw' or instr.lower() == 'jal'):
        imm, r1 = line[2].split("(")
        r1 = r1.replace(')', '')
        if (str(imm).lower() in labels):
            imm = labels[imm.lower()]*4
        out = op + hex(getDecimal(str(imm)))[2:].zfill(4) \
            + hex(registers[r1.lower()])[2:] \
            + hex(registers[line[3].lower()])[2:]
    elif (instr.lower() == 'sw'):
        imm, r1 = line[2].split("(")
        r1 = r1.replace(')', '')
        if (str(imm).lower() in labels):
            imm = labels[imm.lower()]*4
        out = op + hex(getDecimal(str(imm)))[2:].zfill(4) \
            + hex(registers[line[3].lower()])[2:] \
            + hex(registers[r1.lower()])[2:]
    elif (instr.lower == ".word"):
        imm = line[2]
        if (str(imm).lower() in labels):
            imm = labels[imm.lower()]*4
        out = hex(getDecimal(imm))[2:].zfill(8)
    else:
        print("Instruction not found")
        exit(1)

    mifOut += [hex(currAddr)[2:].zfill(8) + ' ; ' + out + ';']
    # print(out)
mifOut += ['END;']

for i in mifOut:
    print(i)


fout.close()