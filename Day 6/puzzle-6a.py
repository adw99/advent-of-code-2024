import sys
from enum import Enum

xword = "MAS"
rows = 0
cols = 0
debug = False

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

def count_stars(grid):
    count = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] in ["*","^"]:
                count += 1
    return count

def print_grid(grid):
    for l in grid:
        print (''.join(l))

if __name__ == '__main__':
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    grid = read_data_file(sys.argv[1])
    rows = len(grid)
    cols = len(grid[0])
    dprint(grid)
    # Enums for directions
    Directions = Enum('Directions', [ ('UP', (0,-1)), ('RIGHT',(1,0)),('DOWN',(0,1)), ('LEFT',(-1,0))])
    NextDir = Enum('Next Direction', [ ('UP', 'RIGHT'), ('RIGHT','DOWN'), ('DOWN','LEFT'), ('LEFT', 'UP')])
    # Initial state
    dir = Directions.UP
    (xpos,ypos) = find_start(grid)
    (xacc,yacc) = dir.value

    exited = False
    while not exited:
        (xacc,yacc) = dir.value
        nextx = xpos + xacc
        nexty = ypos + yacc
        # Does the guard exit?
        if( nextx<0 or nextx>=cols or nexty<0 or nexty>=rows):
            dprint(f"Exiting? {nextx}, {nexty}, {cols}, {rows}")
            exited = True
        # If not can they move forward?
        elif grid[nexty][nextx] != "#":
            grid[nexty][nextx] = "*"
            xpos = nextx
            ypos = nexty
        # else they must turn
        else:
            new_dir = Directions[NextDir[dir.name].value]
            dprint(f"Turning from {dir.name} to {new_dir.name}")
            dir = new_dir
            (xacc,yacc) = dir.value
    
    if debug:
        print_grid(grid)
    total = count_stars(grid)
    print(f"Total: {total}")