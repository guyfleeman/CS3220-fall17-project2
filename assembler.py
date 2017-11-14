#!/usr/bin/python

import sys
import os

if len(sys.argv) < 2:
    print('No file provided')
    exit(1)

nameout = os.path.splitext(sys.argv[1])[0] + '.mif'
nameoutHex = os.path.splitext(sys.argv[1])[0] + '.hex'
if len(sys.argv) >= 3:
    nameout = sys.argv[2]


# Convert number to ensure it is decimal
def getDecimal(numIn, isUpper=False):
    numIn = str(numIn.strip())
    out = 0
    try:
        if numIn.startswith('0X'):
            out = int(numIn[2:], 16)
        else:
            out = int(numIn)
    except ValueError:
        raise ValueError('Invalid number or label: ' + numIn)

    if abs(out) >= 1<<32:
        raise ValueError('Immediate larger than 32bits: ' + numIn)

    if (out < 0):
        # Two's complement if less than 0
        out = -(-out - (1<<32))

    if (isUpper):
        out = (out >> 16) & 0xFFFF
    else:
        out = out & 0xFFFF

    # print(str(numIn) + " - " + str(out))
    return out



lines = []
labels = {}
usedAddr = []

try:
    with open(sys.argv[1]) as f:
        lastAddr = 0
        currAddr = 0
        lineCount = 0
        for line in f:
            lineOriginal = line.strip()
            lineCount += 1
            label = ''

            # Clean and check for empty lines, remove comments
            line = line.replace('\n','')
            line = line.upper()
            line = line.split(';',1)[0]
            if (line.strip() == ''):
                continue

            # Extract labels
            l1 = line.split(':', 1)
            if (len(l1) == 2):
                line = l1[1].strip()
                label = l1[0].strip()
                labels[label] = currAddr
                if line == '':
                    continue

            if len(line) > 0:
                # Split at first space and commas and clean up
                line = line.split(None, 1)
                line = line[0:-1] + line[-1].split(',')
                line = [i.strip() for i in line]
                lineNext = ''
                # Psuedo and special assembler instructions
                if (len(line) == 2 and line[0] == '.ORIG'):
                    # handle .orig
                    usedAddr += [[lastAddr, currAddr-1]]
                    currAddr = getDecimal(line[1])/4
                    lastAddr = currAddr
                    continue
                elif (len(line) == 2 and line[0] == '.NAME'):
                    # handle .name
                    try:
                        label, labelAddrTemp = line[1].split('=');
                        labelAddr = labelAddrTemp
                        labels[label.strip()] = labelAddr
                    except ValueError:
                        raise ValueError("Invalid .NAME input")
                    continue
                elif (len(line) == 2 and line[0] == 'BR' or line[0] == 'B'):
                    line = ['BEQ', line[1], 'R6', 'R6']
                elif (len(line) == 3 and line[0] == 'NOT'):
                    line = ['NAND', line[1], line[1], line[2]]
                elif (len(line) == 4 and line[0] == 'BLE'):
                    line = ['LTE', line[2], line[3], 'R6']
                    lineNext = ['BNEZ', line[1], 'R6']
                elif (len(line) == 4 and line[0] == 'BGE'):
                    line = ['GTE', line[2], line[3], 'R6']
                    lineNext = ['BNEZ', line[1], 'R6']
                elif (len(line) == 2 and line[0] == 'CALL'):
                    line = ['JAL', line[1], 'RA']
                elif (len(line) == 1 and line[0] == 'RET'):
                    line = ['JAL', '0(RA)', 'R9']
                elif (len(line) == 1 and line[0] == 'JMP'):
                    line = ['JAL', line[1], 'R9']

                lines.append([[currAddr] + line, 'Line ' + str(lineCount) + ', \"'
                    + lineOriginal + '\"'])
                currAddr += 1
                if (lineNext != ''):
                    lines.append([[currAddr] + lineNext, 'Line ' +
                        str(lineCount) + ', \"' + lineOriginal])
                    currAddr += 1
            else:
                raise ValueError("Empty value")
except ValueError as inst:
    print(str(inst) + "\n  " + 'Line ' + str(lineCount) + ', \"' + lineOriginal)
    exit(1)
except IOError as inst:
    print("Invalid input file")
    exit(1)

usedAddr += [[lastAddr, currAddr-1]]
# print(labels)

opcodes = {
    'ADD'   : '0011 1111',
    'SUB'   : '0010 1111',
    'AND'   : '0111 1111',
    'OR'    : '0110 1111',
    'XOR'   : '0101 1111',
    'NAND'  : '1011 1111',
    'NOR'   : '1010 1111',
    'XNOR'  : '1001 1111',

    'ADDI'  : '0011 1011',
    'SUBI'  : '0010 1011',
    'ANDI'  : '0111 1011',
    'ORI'   : '0110 1011',
    'XORI'  : '0101 1011',
    'NANDI' : '1011 1011',
    'NORI'  : '1010 1011',
    'XNORI' : '1001 1011',
    'MVHI'  : '1111 1011',

    'LW'    : '0000 1001',
    'SW'    : '0000 1000',

    'F'     : '0011 1110',
    'EQ'    : '1100 1110',
    'LT'    : '1101 1110',
    'LTE'   : '0010 1110',
    'T'     : '1111 1110',
    'NE'    : '0000 1110',
    'GTE'   : '0001 1110',
    'GT'    : '1110 1110',

    'FI'    : '0011 1010',
    'EQI'   : '1100 1010',
    'LTI'   : '1101 1010',
    'LTEI'  : '0010 1010',
    'TI'    : '1111 1010',
    'NEI'   : '0000 1010',
    'GTEI'  : '0001 1010',
    'GTI'   : '1110 1010',

    'BF'    : '0011 0000',
    'BEQ'   : '1100 0000',
    'BLT'   : '1101 0000',
    'BLTE'  : '0010 0000',
    'BEQZ'  : '1000 0000',
    'BLTZ'  : '1001 0000',
    'BLTEZ' : '0110 0000',
    'BT'    : '1111 0000',
    'BNE'   : '0000 0000',
    'BGTE'  : '0001 0000',
    'BGT'   : '1110 0000',
    'BNEZ'  : '0100 0000',
    'BGTEZ' : '0101 0000',
    'BGTZ'  : '1010 0000',

    'JAL'   : '0000 0001'
}

registers = {'R%d' % i : i for i in range(16)}
registers['A0'] = 0;
registers['A1'] = 1;
registers['A2'] = 2;
registers['A3'] = 3;
registers['RV'] = 3;
registers['T0'] = 4;
registers['T1'] = 5;
registers['S0'] = 6;
registers['S1'] = 7;
registers['S2'] = 8;
registers['GP'] = 12;
registers['FP'] = 13;
registers['SP'] = 14;
registers['RA'] = 15;

opRRR = ['ADD', 'SUB', 'AND', 'OR', 'XOR', 'NAND', 'NOR', 'XNOR', 'F', 'EQ',
         'LT', 'LTE', 'T', 'NE', 'GTE', 'GT']
opIRR = ['ADDI', 'SUBI', 'ANDI', 'ORI', 'XORI', 'NANDI', 'NORI', 'XNORI', 'FI',
         'EQI', 'LTI', 'LTEI', 'TI', 'NEI', 'GTEI', 'GTI', 'BF', 'BEQ', 'BLT',
         'BLTE', 'BT', 'BNE', 'BGTE', 'BGT']
opIR = ['MVHI', 'BEQZ', 'BLTZ', 'BLTEZ', 'BNEZ', 'BGTEZ', 'BGTZ']
opPCRel = ['BF', 'BEQ', 'BLT', 'BLTE', 'BEQZ', 'BLTZ', 'BLTEZ', 'BT', 'BNE',
           'BGTE', 'BGT', 'BNEZ', 'BGTEZ', 'BGTZ']
# specials: LW SW JAL

mifOut = []
mifOut += ['WIDTH=32;']
mifOut += ['DEPTH=2048;']
mifOut += ['ADDRESS_RADIX=HEX;']
mifOut += ['DATA_RADIX=HEX;']
mifOut += ['CONTENT BEGIN']

def hexReg(reg):
    try:
        return hex(registers[reg])[2:]
    except KeyError:
        raise ValueError("Invalid register value: " + str(reg))

instrHex = {}

for l1 in lines:
    try:
        line = l1[0]
        info = l1[1]
        currAddr = line[0]
        instr = line[1]
        if instr == '.WORD':
            op = ''
        else:
            try:
                op = hex(int(opcodes[instr].replace(' ', ''), 2))[2:].zfill(2)
            except KeyError:
                raise ValueError("Invalid instruction or parameters")

        out = ''

        if (instr in opRRR and len(line) == 5):
            out = op + '000' + hexReg(line[2]) + hexReg(line[3]) \
                + hexReg(line[4])
        elif (instr in opIRR and len(line) == 5):
            imm = line[2]
            if (str(imm) in labels):
                imm = labels[imm]
                if (instr in opPCRel):
                    # print(str(hex(currAddr)) + " " + str(hex(imm)))
                    imm = (imm*4 - currAddr*4 - 4)/4
            out = op + hex(getDecimal(str(imm)))[2:].zfill(4) \
                + hexReg(line[3]) + hexReg(line[4])
        elif (instr in opIR and len(line) == 4):
            imm = line[2]
            if (str(imm) in labels):
                imm = labels[imm]
                if (instr in opPCRel):
                    # print(str(hex(currAddr)) + " " + str(hex(imm)))
                    imm = (imm*4 - currAddr*4 - 4)/4
            immVal = getDecimal(str(imm), instr=='MVHI')
            out = op + hex(immVal)[2:].zfill(4) + '0' + hexReg(line[3])
        elif ((instr == 'LW' or instr == 'JAL') and len(line) == 4):
            imm, r1 = line[2].split('(')
            r1 = r1.replace(')', '')
            if (str(imm) in labels):
                imm = labels[imm]
            out = op + hex(getDecimal(str(imm)))[2:].zfill(4) + hexReg(r1) \
                + hexReg(line[3])
        elif (instr == 'SW' and len(line) == 4):
            imm, r1 = line[2].split('(')
            r1 = r1.replace(')', '')
            if (str(imm) in labels):
                imm = labels[imm]
            out = op + hex(getDecimal(str(imm)))[2:].zfill(4) \
                + hexReg(line[3]) + hexReg(r1)
        elif (instr == '.WORD' and len(line) == 3):
            imm = line[2]
            if (str(imm) in labels):
                imm = labels[imm]
            out = hex(getDecimal(imm))[2:].zfill(8)
        else:
            raise ValueError("Invalid instruction or parameters")

        out = out.replace('L','') # TODO why needed?
        instrHex[currAddr] = out;
        mifOut += [hex(currAddr)[2:].zfill(8) + ' : ' + out + ';']
        # print(out)
    except ValueError as inst:
        print(str(inst) + "\n  " + str(info))
        exit(1)

deadAddr = []

lastUsed = -1
for i in range(2048):
    used = False
    for j in usedAddr:
        if i >= j[0] and i <= j[1]:
            used = True
            break
    if used:
        if i != lastUsed+1:
            deadAddr += [[lastUsed+1, i-1]]
        lastUsed = i
if lastUsed != 2047:
    deadAddr += [[lastUsed+1, 2047]]

for i in deadAddr:
    mifOut += ['[' + hex(i[0])[2:].zfill(8) + '..' + hex(i[1])[2:].zfill(8)
                + '] : DEAD;']

mifOut += ['END']

# for i in mifOut:
#     print(i)

with open(nameout, 'w') as fout:
    for i in mifOut:
        fout.write(i+'\n')

with open(nameoutHex, 'w') as fout:
    for i in range(2048):
        if i in instrHex:
            fout.write(instrHex[i] + "\n")
        else:
            fout.write("0000DEAD" + "\n")
