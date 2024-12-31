import sys
import re


debug = False

def dprint(fs):
    if debug:
        print(fs)

def read_data_file(fname):
    reg_rex = re.compile("Register (.): (\d+)")
    
    df = open(fname, "r")
    lines = df.read().splitlines()
    registers = {}
    instructions = []
    for l in lines:
        if 'Register' in l:
            m = reg_rex.search(l)
            registers[m[1]] = int(m[2])
        elif 'Program' in l:
            instructions = [int(i) for i in l.removeprefix('Program: ').split(',')]

    return registers, instructions

def process_operand(op,registers):
    if op in [0,1,2,3]:
        return op
    elif op in [4,5,6]:
        reg = chr( ord('A') + (op-4) )
        return registers[reg]
    else:
        return 0

def process_instruction(ins,opc,registers):
    output = ''
    jump = -1
    combo = process_operand(opc,registers)
    if ins == 0:
        registers['A'] = int( registers['A'] / pow(2,combo) )
        # dprint(f"adv {combo} -> {registers} ({pow(2,combo)})")
    elif ins == 1:
        registers['B'] ^= opc
        # dprint(f"bxl {opc}  -> {registers}")
    elif ins == 2:
        registers['B'] = combo % 8
        # dprint(f"bst {combo} -> {registers}")
    elif ins == 3:
        if registers['A'] != 0:
            jump = opc
        # dprint(f"jmp ({opc}): {jump}")
    elif ins == 4:
        registers['B'] ^= registers['C']
        # dprint(f"bxc  -> {registers}")
    elif ins == 5:        
        output = str(combo % 8)
        # dprint(f"out {output} -> {registers}")
    elif ins == 6:
        registers['B'] = int( registers['A'] / pow(2,combo) )
        # dprint(f"bdv {combo} -> {registers}")
    elif ins == 7:
        registers['C'] = int( registers['A'] / pow(2,combo) )
        # dprint(f"cdv {combo} -> {registers}")


    return output, jump

if __name__ == '__main__':
    button_costs = [3,1]
    print(f"*** Day 17, Part 1 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    registers, instructions = read_data_file(sys.argv[1])
    dprint(f"Registers: {registers}")
    dprint(f"Program: {instructions}")
    output = ''
    i = 0
    while i < len(instructions):
        ins = instructions[i]
        opc = instructions[i+1]
        preva = registers['A']
        prevb = registers['B']
        prevc = registers['C']
        out,jump = process_instruction(ins,opc,registers)
        if out!='':
            dprint(f"OUT: {out} vs A: {preva%8}, {prevb%8}, {prevc%8} -> ({registers})")

        if out != '':            
            if output != '':
                output += ','
            output += out
        if jump !=-1:
            i = jump
        else:
            i += 2
    print(f"Output: {output}")
    dprint(f"Final registers: {registers}")