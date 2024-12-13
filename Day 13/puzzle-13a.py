import sys
import re
import numpy as np

debug = False

def dprint(fs):
    if debug:
        print(fs)

def read_data_file(fname):

    button_rex = re.compile("Button (A|B): X\\+(\d+), Y\\+(\d+)")
    prize_rex = re.compile("Prize: X\\=(\\d+), Y\\=(\\d+)")

    df = open(fname, "r")
    fs = df.read()
    lines = fs.split('\n')
    curr_machine = {}
    machines = [curr_machine]
    for l in lines:
        if 'Button' in l:
            m = button_rex.search(l)
            curr_machine[m[1]] = [int(m[2]), int(m[3])]
        elif 'Prize' in l:
            m = prize_rex.search(l)
            curr_machine['prize'] = [int(m[1]),int(m[2])]
        else:
            # blank line, get ready for next machine
            curr_machine = {}
            machines.append(curr_machine)
    return machines

def check_count(x):
    # As per challenge, button counts should not exceed 100
    # Also if the math returns something not integer-shaped, we
    # can't win this prize. I'm checking that to 3 digits here.
    return x<=100.0 and int(x*1000)%1000 == 0 

def solve_for_machine(m1):
    global button_costs
    dprint(f"Machine: {m1}")
    ba = m1['A']
    bb = m1['B']

    a1 = np.matrix([ [ba[0],bb[0] ], [ba[1],bb[1]]])
    a1_invert = np.linalg.inv(a1)

    p = m1['prize']
    a2 = np.matrix( [ [p[0]], [p[1]]] )
    result = a1_invert * a2

    dprint(f"Result: {result}")
    dprint(f"Result2: {result[0].tolist()}")
    acount = result[0][0]
    bcount = result[1][0]
    dprint(f"?>{acount},{bcount} - {type(acount)}")
    if check_count(acount) and check_count(bcount):
        return acount * button_costs[0] + bcount * button_costs[1]
    else:
        return 0

if __name__ == '__main__':
    button_costs = [3,1]
    print(f"*** Day 13, Part 1 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True

    machines = read_data_file(sys.argv[1])
    dprint(f"Machines({len(machines)}): {machines}")
    total = 0
    prizes = 0
    # for m in machines:
    #     tokens = solve_for_machine(m)
    #     if tokens !=0:
    #         prizes += 1
    #         total += tokens
    solve_for_machine(machines[0])
    print(f"We need {total} tokens to win {prizes} prizes")

    
