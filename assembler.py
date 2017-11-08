#!/usr/bin/python

import sys
import os

if len(sys.argv) < 2:
    print('No file provided')
    exit(1)

nameout = os.path.splitext(sys.argv[1])[0] + '.mif'
if len(sys.argv) >= 3:
    nameout = sys.argv[2]



# Convert number to ensure it is decimal
def getDecimal(numIn):
    numIn = str(numIn.strip())
    out = 0
    try:
        if numIn.startswith('0X'):
            out = int(numIn[2:], 16)
        else:
            out = int(numIn)
    except ValueError:
        raise ValueError('Invalid number or label: ' + numIn)

    if abs(out) >= 1<<16:
        raise ValueError('Immediate larger than 16bits: ' + numIn)

    if (out < 0):
        # Two's complement if less than 0
        out = -(-out - (1<<16))

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
                        labelAddr = getDecimal(labelAddrTemp)/4
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

opcodes = {
    'ADD'   : '1111 0011',
    'SUB'   : '1111 0010',
    'AND'   : '1111 0111',
    'OR'    : '1111 0110',
    'XOR'   : '1111 0101',
    'NAND'  : '1111 1011',
    'NOR'   : '1111 1010',
    'XNOR'  : '1111 1001',

    'ADDI'  : '1011 0011',
    'SUBI'  : '1011 1011',
    'ANDI'  : '1011 0111',
    'ORI'   : '1011 0110',
    'XORI'  : '1011 0101',
    'NANDI' : '1011 1011',
    'NORI'  : '1011 1010',
    'XNORI' : '1011 1001',
    'MVHI'  : '1011 1001',

    'LW'    : '1000 0000',
    'SW'    : '1001 0000',

    'F'     : '1110 0011',
    'EQ'    : '1110 1100',
    'LT'    : '1110 1101',
    'LTE'   : '1110 0010',
    'T'     : '1110 1111',
    'NE'    : '1110 0000',
    'GTE'   : '1110 0001',
    'GT'    : '1110 1110',

    'FI'    : '1010 0011',
    'EQI'   : '1010 1100',
    'LTI'   : '1010 1101',
    'LTEI'  : '1010 0010',
    'TI'    : '1010 1111',
    'NEI'   : '1010 0000',
    'GTEI'  : '1010 0001',
    'GTI'   : '1010 1110',

    'BF'    : '0000 0011',
    'BEQ'   : '0000 1100',
    'BLT'   : '0000 1101',
    'BLTE'  : '0000 0010',
    'BEQZ'  : '0000 1000',
    'BLTZ'  : '0000 1001',
    'BLTEZ' : '0000 0110',
    'BT'    : '0000 1111',
    'BNE'   : '0000 0000',
    'BGTE'  : '0000 0001',
    'BGT'   : '0000 1110',
    'BNEZ'  : '0000 0100',
    'BGTEZ' : '0000 0101',
    'BGTZ'  : '0000 1010',

    'JAL'   : '0001 0000'
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
                imm = labels[imm]*4
                if (instr in opPCRel):
                    imm = imm - currAddr - 4
            out = op + hex(getDecimal(str(imm)))[2:].zfill(4) \
                + hexReg(line[3]) + hexReg(line[4])
        elif (instr in opIR and len(line) == 4):
            imm = line[2]
            if (str(imm) in labels):
                imm = labels[imm]*4
            out = op + hex(getDecimal(str(imm)))[2:].zfill(4) \
                + hexReg(line[3]) + '0'
        elif ((instr == 'LW' or instr == 'JAL') and len(line) == 4):
            imm, r1 = line[2].split('(')
            r1 = r1.replace(')', '')
            if (str(imm) in labels):
                imm = labels[imm]*4
            out = op + hex(getDecimal(str(imm)))[2:].zfill(4) + hexReg(r1) \
                + hexReg(line[3])
        elif (instr == 'SW' and len(line) == 4):
            imm, r1 = line[2].split('(')
            r1 = r1.replace(')', '')
            if (str(imm) in labels):
                imm = labels[imm]*4
            out = op + hex(getDecimal(str(imm)))[2:].zfill(4) \
                + hexReg(line[3]) + hexReg(r1)
        elif (instr == '.WORD' and len(line) == 3):
            imm = line[2]
            if (str(imm) in labels):
                imm = labels[imm]*4
            out = hex(getDecimal(imm))[2:].zfill(8)
        else:
            raise ValueError("Invalid instruction or parameters")

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

mifOut += ['END;']

# for i in mifOut:
#     print(i)

with open(nameout, 'w') as fout:
    for i in mifOut:
        fout.write(i+'\n')
