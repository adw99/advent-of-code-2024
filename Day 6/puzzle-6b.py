import sys
import copy
from enum import Enum

xword = "MAS"
rows = 0
cols = 0
debug = False
xstart = 0
ystart = 0
# Enums for directions
Directions = Enum('Directions', [ ('UP', (0,-1)), ('RIGHT',(1,0)),('DOWN',(0,1)), ('LEFT',(-1,0))])
NextDir = Enum('Next Direction', [ ('UP', 'RIGHT'), ('RIGHT','DOWN'), ('DOWN','LEFT'), ('LEFT', 'UP')])

def dprint(fs):
    if debug:
        print(fs)

def read_data_file(fname):
    df = open(fname, "r")
    fs = df.read()
    lines = fs.split('\n')
    grid = [list(i) for i in lines]
    dprint(f"Lines: {len(lines)}, Cols: {len(lines[0])}")

    return grid

def find_start(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "^":
                dprint(f"Start pos: {x}, {y}")
                return (x,y)
    return (-1,-1)

def run_grid(grid):
    # Initial state
    dir = Directions.UP
    xpos = xstart
    ypos = ystart
    (xacc,yacc) = dir.value
    grid[ypos][xpos] = "*"

    exited = False
    looped = False
    turns = []
    while not exited and not looped:
        (xacc,yacc) = dir.value
        nextx = xpos + xacc
        nexty = ypos + yacc
        # Does the guard exit?
        if( nextx<0 or nextx>=cols or nexty<0 or nexty>=rows):
            # dprint(f"Exiting? {nextx}, {nexty}, {cols}, {rows}")
            exited = True
        # If not can they move forward?
        elif grid[nexty][nextx] not in ["#", "X"]:
            grid[nexty][nextx] = "*"
            xpos = nextx
            ypos = nexty
        # else they must turn
        else:            
            new_dir = Directions[NextDir[dir.name].value]
            # have we made this turn before? if so it's a loop
            new_turn = ( dir.name, new_dir.name, nextx, nexty)
            if( new_turn in turns):
                looped = True
                break
            else:
                turns.append(new_turn)
            # dprint(f"Turning from {dir.name} to {new_dir.name}")
            dir = new_dir
            (xacc,yacc) = dir.value
    return looped

def print_grid(grid):
    if debug:
        for l in grid:
            print (''.join(l))

def count_stars(grid):
    count = 0
    for x in range(cols):
        for y in range(rows):
            if grid[y][x] == "#":
                count+=1 
    dprint(f"Obstacles: {count}")
    return count

def find_loops(o_grid):
    attempts = 0
    loops = 0
    # Brute force o(N^2) solution
    for y in range(rows):
        for x in range(cols):
            if( o_grid[y][x] not in ["#","^"]):
                # turn test point into an obstance and test the modified grid
                grid = copy.deepcopy(o_grid)
                grid[y][x] = "X"
                dprint(f"Changing ({x},{y})")                
                print_grid(grid)
                attempts += 1
                if run_grid(grid):
                    loops += 1                
                    dprint(f"Loop found! changed({x},{y})")
                grid[y][x] = "."
    return(loops,attempts)

if __name__ == '__main__':
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    grid = read_data_file(sys.argv[1])
    rows = len(grid)
    cols = len(grid[0])    
    (xstart,ystart) = find_start(grid)
    expected_runs = (rows * cols) - (count_stars(grid) + 1)   
    print_grid(grid)
    (loops,attempts) = find_loops(grid)
    print(f"Loop created by changing {loops} positions. Runs: {attempts} / {expected_runs}")
    if debug:
        print_grid(grid)

