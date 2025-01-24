import sys
import re
from collections import defaultdict

debug = False

def dprint(fs):
    if debug:
        print(fs)

def lockvskey(curr,locks,keys):
    if curr[0].startswith('###'):
        locks.append(curr)
    else:
        keys.append(curr)
    return locks,keys

def read_data_file(fname):
    rule_rex = re.compile("(.{3}) (\\w*) (.{3}) -> (.{3})")
    df = open(fname, "r")
    lines = df.read().splitlines()
    keys = []
    locks = []
    count = 0
    curr = []
    for l in lines:
        if l != '':
            curr.append(l)
        else:
            locks,keys = lockvskey(curr,locks,keys)
            curr = []
    locks,keys = lockvskey(curr,locks,keys)
    return locks,keys


def transform(grid):
    pins = len(grid[0])
    result = []
    for p in range(pins):

        count = -1  # to not count top/bottom row
        for g in range(len(grid)):
            if grid[g][p] == '#':
                count += 1
        result.append(count)
    return result



if __name__ == '__main__':
    print(f"*** Day 24, Part 2 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    fname = sys.argv[1] if len(sys.argv) >=2 else 'sample.txt' 
    tlocks,tkeys = read_data_file(fname)

    locks = [ transform(i) for i in tlocks]
    keys = [ transform(k) for k in tkeys]
    dprint(f"Locks: {len(locks)}")
    dprint(f"Keys: {len(keys)}")

    # count non overlapping key/lock combs
    count = 0
    threshold = 5
    for l in locks:
        for k in keys:
            overlap = False
            for i in range(len(l)):
                if l[i] + k[i] > threshold:
                    overlap = True
            if not overlap:
                count += 1
    print(f"Non-overlapping key/lock combos: {count}")
