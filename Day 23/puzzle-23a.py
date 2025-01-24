import sys
from collections import defaultdict

debug = False

def dprint(fs):
    if debug:
        print(fs)

def read_data_file(fname):  
    df = open(fname, "r")
    lines = df.read().splitlines()
    inputs = []
    for l in lines:
        m = l.split('-')        
        inputs.append( (m[0],m[1] ))

    return inputs

def build_connections(pairs):
    connections = defaultdict(list)
    for (p1,p2) in pairs:
        connections[p1].append(p2)
        connections[p2].append(p1)

    csets = {}
    for k in connections.keys():
        csets[k] = set(connections[k])
    return csets

if __name__ == '__main__':
    print(f"*** Day 23, Part 1 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    fname = sys.argv[1] if len(sys.argv) >=2 else 'sample.txt' 
    pairs = read_data_file(fname)
    connections = build_connections(pairs)
    nodes = connections.keys()

    cliques = []
    dprint(connections)
    for p1 in nodes:
        for p2 in connections[p1]:
            common = connections[p1] & connections[p2]
            for p3 in common:
                # dprint(f"{p1} and {p2} have {p3} in common")
                c = [p1,p2,p3]
                c.sort()
                if c not in cliques:
                    cliques.append( c )

    dprint(f"Cliques: {len(cliques)}")

    count = 0
    matches = []
    for n in nodes:
        if n.startswith('t'):
            for c in cliques:
                if n in c and c not in matches:
                    matches.append(c)
                    count += 1

    dprint(matches)
    print(f"Cliques with computers whose name begins with t: {count}")
