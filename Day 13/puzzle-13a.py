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
    check = 0.0 < x <=100.0 and abs(x - round(x))<0.1
    return check

def solve_for_machine(m1):
    # dprint(f"Machine: {m1}")
    global button_costs
    ba = m1['A']
    bb = m1['B']

    a1 = np.array([ [ba[0],bb[0] ], [ba[1],bb[1]]])
    a1_i = np.linalg.inv(a1)
    p = m1['prize']
    a2 = np.array( [ p[0], p[1]] )

    result = np.dot(a1_i,a2)
    acount = result[0]
    bcount = result[1]
        
    if check_count(acount) and check_count(bcount):
        return int(round(acount)) * button_costs[0] + int(round(bcount)) * button_costs[1]
    else:
        return 0

if __name__ == '__main__':
    button_costs = [3,1]
    print(f"*** Day 13, Part 1 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True

    machines = read_data_file(sys.argv[1])
    dprint(f"Machine count: {len(machines)}")
    total = 0
    prizes = 0
    for m in machines:
        tokens = solve_for_machine(m)
        if tokens !=0:
            prizes += 1
            total += tokens
    print(f"We need {total} tokens to win {prizes} prizes")

    
