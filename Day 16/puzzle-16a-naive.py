import sys
from enum import Enum
import copy

debug = False
Directions = Enum('Directions', [ ('UP', (0,-1)), ('RIGHT',(1,0)),('DOWN',(0,1)), ('LEFT',(-1,0))])

def dprint(fs):
    if debug:
        print(fs)

def read_data_file(fname):
    df = open(fname, "r")
    fs = df.read()
    lines = fs.split('\n')
    warehouse = []
    for l in lines:
        warehouse.append([r for r in l])
    return warehouse

def print_grid(grid):
    for line in grid:
        print(''.join([str (i) for i in line]))

def print_trail(trail,master_grid):
    grid = copy.deepcopy(master_grid)
    for pt in trail:
        (x,y) = pt
        grid[y][x] = f"{bcolors.OKCYAN}*{bcolors.ENDC}"
    print_grid(grid)

def find_start(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "S":
                return (x,y)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Trail:
    def __init__(self,x,y,dir,trail,turns):
        self.x = x
        self.y = y
        self.dir = dir
        self.trail = trail
        self.turns = turns
    def __str__(self):
        return f" ({self.x},{self.y}) => {self.dir} ({self.turns}: {self.trail})"


def build_starting_options(start,grid):
    options = []
    start_dir = "RIGHT"
    (x,y) = start
    for  d in Directions:
        (xacc,yacc) = d.value        
        if grid[y+yacc][x+xacc] == ".":
            options.append( Trail(x+xacc,y+yacc,d.name,[(x+xacc,y+yacc)],0 if d.name == start_dir else 1))
            dprint(f"New option ({x+xacc},{y+yacc}) => {d.name}")

    return options

def run_grid(start,grid):
    options = build_starting_options(start,grid)
    min_score = 999999
    solutions = []
    pops = 0
    calcs = 0

    while len(options)>0:
        curr = options.pop()
        if calcs % 1000 == 0:
            # input(f"<enter>, trail: {curr.trail}")
            temp_set = set(curr.trail)
            if len(temp_set) != len(curr.trail):
                dprint("Warning - repeated pt in trail (?)")
                dprint(curr.trail)
        pops += 1
        if pops % 100000 == 0:
            if debug:
                print_trail(curr.trail,grid)
            dprint(f"Stack height: {len(options)}, calcs: {calcs}, trail length: {len(curr.trail)}")
        for d in Directions:
            calcs += 1
            (xacc,yacc) = d.value
            nx = curr.x + xacc
            ny = curr.y + yacc
            next = grid[ny][nx]
            # dprint(f">option({curr.x},{curr.y}) => {d.name} = {next}")
            if next != "#":
                new_trail = curr.trail.copy()
                new_trail.append((nx,ny))
                new_turns = curr.turns if d.name == curr.dir else curr.turns + 1
                new_trail = Trail(nx,ny,d.name,new_trail,new_turns)
                if( next =='.' and (nx,ny) not in curr.trail):
                    # new option
                    # dprint(f"New option ({nx},{ny}) => {d.name}")
                    curr_score = score_trail(new_trail)
                    if curr_score < min_score:
                        options.append( new_trail )
                elif next == "E":
                    # we found the end
                    score = score_trail(new_trail)
                    if score < min_score:
                        min_score = score
                        dprint(f">>New min score: {score}")
                    solutions.append( new_trail )

    return solutions                

def score_trail(t):
    return 1000*t.turns + len(t.trail)

if __name__ == '__main__':
    button_costs = [3,1]
    print(f"*** Day 16, Part 1 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    grid = read_data_file(sys.argv[1])
    start = find_start(grid)
    if debug:
        print_grid(grid)
        print(f"Start: {start}")
    print("Solving....")
    solutions = run_grid(start,grid)
    print(f"Solutions found: {len(solutions)}")

    count = 1
    min_score = 9999999
    winner = None
    win_list = []
    for s in solutions:
        score = 1000*s.turns + len(s.trail)
        if score < min_score:
            min_score = score
            winner = s
            win_list = [s]
        elif score == min_score:
            win_list.append(s)
        dprint(f"{count}) steps: {len(s.trail)}, score: {score}")
        count += 1
    dprint(f"Winning trail:")
    print_trail(winner.trail,grid)
    print(f"Lowest score: {min_score}")
    print(f"Equivalent solutions: {len(win_list)}")
