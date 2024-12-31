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

    return registers, instructions, l.removeprefix('Program: ')

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
        dprint(f"adv {combo} -> {registers} ({pow(2,combo)})")
    elif ins == 1:
        registers['B'] = registers['B']^opc
        dprint(f"bxl {opc}  -> {registers}")
    elif ins == 2:
        registers['B'] = combo % 8
        dprint(f"bst {combo} -> {registers}")
    elif ins == 3:
        if registers['A'] != 0:
            jump = opc
        dprint(f"jmp ({opc}): {jump}")
    elif ins == 4:
        registers['B'] = registers['B']^registers['C']
        dprint(f"bxc  -> {registers}")
    elif ins == 5:        
        output = str(combo % 8)
        dprint(f"out {output} -> {registers}")
    elif ins == 6:
        registers['B'] = int( registers['A'] / pow(2,combo) )
        dprint(f"bdv {combo} -> {registers}")
    elif ins == 7:
        registers['C'] = int( registers['A'] / pow(2,combo) )
        dprint(f"cdv {combo} -> {registers}")


    return output, jump

def run_program(instructions,registers,program):
    output = ''
    i = 0
    while i < len(instructions):
        ins = instructions[i]
        opc = instructions[i+1]
        out,jump = process_instruction(ins,opc,registers)

        if out != '':            
            if output != '':
                output += ','
            output += out
            # if not program.startswith(output):
            #     break                        
        if jump !=-1:
            i = jump
        else:
            i += 2
    return output
    
if __name__ == '__main__':
    button_costs = [3,1]
    print(f"*** Day 17, Part 2 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    registers, instructions, program = read_data_file(sys.argv[1])
    dprint(f"Registers: {registers}")
    dprint(f"Program: {instructions} / {len(instructions)}")
    dprint(f"Target: ({program})")
    nums = [int(i) for i in program.split(',')]

    solutions = []
    options = [ (0,1 )]
    while len(options)>0 and len(solutions)==0:
        val,depth = options.pop(0)
        for i in range(8):
            reg = {}
            reg['A'] = val + i
            reg['B'] = registers['B']
            reg['C'] = registers['C']
            output = run_program(instructions,reg,program)
            if output == program:
                solutions.append(val+i)
            out_nums = [int(i) for i in output.split(',')]
            if out_nums == nums[len(nums)-depth:]:
                dprint(f"Found {val} + {i}: {output}")
                nextval = (val + i) << 3
                options.append( (nextval, depth+1) )

    if len(solutions) == 0:
        print("No solution found")
    else:
        print(f"Solution: {solutions[0]} / {len(solutions)}")
