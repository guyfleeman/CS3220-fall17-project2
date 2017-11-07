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
    print(out)
    if (out < 0):
        out = -(-out - (1<<16))
    print(out)
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
    "add"   : "1111 0011",
    "sub"   : "1111 0010",
    "and"   : "1111 0111",
    "or"    : "1111 0110",
    "xor"   : "1111 0101",
    "nand"  : "1111 1011",
    "nor"   : "1111 1010",
    "xnor"  : "1111 1001",

    "addi"  : "1011 0011",
    "subi"  : "1011 1011",
    "andi"  : "1011 0111",
    "ori"   : "1011 0110",
    "xori"  : "1011 0101",
    "nandi" : "1011 1011",
    "nori"  : "1011 1010",
    "xnori" : "1011 1001",
    "mvhi"  : "1011 1001",

    "lw"    : "1000 0000",
    "sw"    : "1001 0000",

    "f"     : "1110 0011",
    "eq"    : "1110 1100",
    "lt"    : "1110 1101",
    "lte"   : "1110 0010",
    "t"     : "1110 1111",
    "ne"    : "1110 0000",
    "gte"   : "1110 0001",
    "gt"    : "1110 1110",

    "fi"    : "1010 0011",
    "eqi"   : "1010 1100",
    "lti"   : "1010 1101",
    "ltei"  : "1010 0010",
    "ti"    : "1010 1111",
    "nei"   : "1010 0000",
    "gtei"  : "1010 0001",
    "gti"   : "1010 1110",

    "bf"    : "0000 0011",
    "beq"   : "0000 1100",
    "blt"   : "0000 1101",
    "blte"  : "0000 0010",
    "beqz"  : "0000 1000",
    "bltz"  : "0000 1001",
    "bltez" : "0000 0110",
    "bt"    : "0000 1111",
    "bne"   : "0000 0000",
    "bgte"  : "0000 0001",
    "bgt"   : "0000 1110",
    "bnez"  : "0000 0100",
    "bgtez" : "0000 0101",
    "bgtz"  : "0000 1010",

    "jal"   : "0001 0000"
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
    elif (instr.lower() == ".word"):
        out = hex(getDecimal(line[2]))[2:].zfill(8)
    else:
        print(instr)
        print("Instruction not found")
        exit(1)

    mifOut += [hex(currAddr)[2:].zfill(8) + ' ; ' + out + ';']
    # print(out)
mifOut += ['END;']

for i in mifOut:
    print(i)


fout.close()
