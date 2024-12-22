import sys

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

cache = { '': 1}
def solve_design(design):
    global patterns
    if design in cache:
        return cache[design]
    else:         
        val = sum(
            solve_design( design.removeprefix(p) )
            for p in patterns
            if design.startswith(p)
        )
        cache[design] = val
        return val

if __name__ == '__main__':
    button_costs = [3,1]
    print(f"*** Day 19, Part 2 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    fname = sys.argv[1] if len(sys.argv) >=2 else 'sample.txt' 
    patterns,designs = read_data_file(fname)

    dprint(f"Designs: {len(designs)}")
    dprint(f"Patterns: {len(patterns)}")
    count = 0
    dc = 0
    for d in designs:
        dc += 1
        if dc % 10 == 0:
            dprint(f">{dc}")
        solutions = solve_design(d)        
        dprint(f"Design {d} => {solutions}")
        count += solutions

    print(f"{count} solutions are available")
