import sys
from enum import Enum
import copy
import heapq
import math
from collections import defaultdict

debug = False

def dprint(fs):
    if debug:
        print(fs)

def read_data_file(fname):
    patterns = []
    designs = []
    df = open(fname, "r")
    lines = df.read().splitlines()
    for l in lines:
        if ',' in l:
            patterns = [x.strip() for x in l.split(',')]
        elif len(l.strip())>0:
            designs.append(l.strip())
    return patterns,designs

def solve_design(design,patterns):
    opt = (design,[])
    q = [opt]
    while len(q)>0:
        d,trail = q.pop()
        for p in patterns:
            if d == p:
                trail.append(d)
                return True,trail
            elif d.startswith(p):
                new_trail = trail.copy()
                new_trail.append(p)
                nd = d.removeprefix(p)
                q.append((nd,new_trail))                
    return False, []

if __name__ == '__main__':
    button_costs = [3,1]
    print(f"*** Day 19, Part 1 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    fname = sys.argv[1] if len(sys.argv) >=2 else 'sample.txt' 
    patterns,designs = read_data_file(fname)

    dprint(f"Designs: {designs}")
    dprint(f"Patterns: {patterns}")
    count = 0
    for d in designs:
        p, trail = solve_design(d,patterns)

        if p:
            dprint(f"Design {d} => {trail}")
            count += 1
        else:
            dprint(f"Design {d} not solvable")

    print(f"{count} designs can be implemented")
