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
        v = [m[0],m[1]]
        v.sort()        
        inputs.append( (v[0],v[1]) )
    return inputs

def build_connections(pairs):
    connections = defaultdict(set)
    for (p1,p2) in pairs:
        connections[p1].add(p2)
        connections[p2].add(p1)
    final = {key: set(connections[key]) for key in connections.keys()}
    return final

def BronKerbosch(R, P, X, graph):
    if len(P) == 0 and len(X) == 0:
        yield R
    while len(P)>0:
        v = P.pop()
        yield from BronKerbosch( R.union({v}),
                                 P.intersection(graph[v]),
                                 X.intersection(graph[v]),
                                 graph
                                )


def find_max_clique(nodes,connections):
    R = set()
    X = set()
    P = set(nodes)

    all_cliques = list(BronKerbosch(R,P,X,connections))
    dprint(f"Cliques found: {len(all_cliques)}")
    max = -1
    max_clique = None
    for c in all_cliques:
        if len(c) > max:
            max = len(c)
            max_clique = c
    
    return max_clique

def set_to_password(clique):
    cl = list(clique)
    cl.sort()
    return ','.join(cl)

if __name__ == '__main__':
    print(f"*** Day 23, Part 2 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    fname = sys.argv[1] if len(sys.argv) >=2 else 'sample.txt' 
    pairs = read_data_file(fname)
    connections = build_connections(pairs)
    nodes = connections.keys()

    max_clique = find_max_clique(nodes,connections)

    print(f"Maximun cliques size: {len(max_clique)}, password: {set_to_password(max_clique)}")
    
