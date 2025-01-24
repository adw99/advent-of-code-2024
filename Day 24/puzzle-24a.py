import sys
import re
from collections import defaultdict

debug = False

def dprint(fs):
    if debug:
        print(fs)

def read_data_file(fname):
    rule_rex = re.compile("(.{3}) (\\w*) (.{3}) -> (.{3})")
    df = open(fname, "r")
    lines = df.read().splitlines()
    values = {}
    rules = {}
    for l in lines:
        if ':' in l:
            m = l.split(':')        
            values[m[0]] = bool(int(m[1]))
        elif '->' in l:
            m = rule_rex.search(l)
            rules[m[4]] = (m[1],m[2],m[3])
            values[m[4]] = None
    return values,rules

def eval_node(rule,values):
    (al,op,bl) = rule
    a = values[al]
    b = values[bl]
    if a == None or b == None:        
        return None
    if op == 'AND':
        return a and b
    elif op == 'OR':
        return a or b
    elif op == 'XOR':
        return a ^ b
    else:
        raise ValueError('Invalid operation: {op}')

def extract_value(prefix,values):
    v_nodes = [i for i in values.keys() if i.startswith(prefix)]
    result = 0
    for n in v_nodes:
        val = values[n]
        if val:
            result += 1 << int(n.removeprefix(prefix))
    return result

if __name__ == '__main__':
    print(f"*** Day 24, Part 1 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    fname = sys.argv[1] if len(sys.argv) >=2 else 'sample.txt' 
    values,rules = read_data_file(fname)
    dprint(f"Values ({len(values)}): {values}")
    dprint(f"Rules ({len(rules)}): {rules}")
    nodes = rules.keys()
    working = True
    passes = 0
    while working and passes<99:
        passes += 1
        calcs = 0
        more_work = False
        for n in nodes:
            values[n] = eval_node(rules[n],values)
            if values[n] == None:
                more_work = True
            else:
                calcs += 1
        working = more_work
        print(f"Pass {passes}, calcs: {calcs} of {len(rules)}")
    print(f"X : {extract_value('x',values)}")
    print(f"Y : {extract_value('y',values)}")
    print(f"Z : {extract_value('z',values)}")

    