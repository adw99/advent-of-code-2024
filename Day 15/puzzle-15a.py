import sys
import re
import copy 
import math
from enum import Enum

debug = False

def dprint(fs):
    if debug:
        print(fs)

def read_data_file(fname):
    line_rex = re.compile("p=(\\d+),(\\d+) v=(-?\\d+),(-?\\d+)")

    df = open(fname, "r")
    fs = df.read()
    lines = fs.split('\n')
    warehouse = []
    moves = ""
    for l in lines:
        if l.startswith('#'):
            warehouse.append([r for r in l])
        else:
            moves += l
    return warehouse,[m for m in moves]

def find_robot(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == '@':
                return (x,y)
    return (-1,-1)


Directions = Enum('Directions', [ ('^', (0,-1)), ('>',(1,0)),('v',(0,1)), ('<',(-1,0))])

def next_pos(start,dir):
    global Directions
    (x,y) = start
    (dx,dy) = Directions[dir].value
    return (x+dx,y+dy)

def can_move(m,start,warehouse):
    (x,y) = start
    (nx,ny) = next_pos(start,m)
    if warehouse[ny][nx] == '.':
        # dprint(f"Can move ({start}) {m}: True")
        return True
    elif warehouse [ny][nx] == "O":
        return can_move(m,(nx,ny),warehouse)
    else:
        # dprint(f"Can move ({start}) {m}: False")
        return False

def move(m,start,warehouse):
    dprint(f"Move {start},{m}")
    (nx,ny) = next_pos(start,m)
    next = warehouse[ny][nx]
    if  next == "O":
        # crate, assume we can move it
        move(m,(nx,ny),warehouse)
        swap(start,(nx,ny),warehouse)
    elif next == ".":
        swap(start,(nx,ny),warehouse)
    else:
        #shouldn't happen (?)
        print(f"**** Cannot move into {next}")
    
def swap(a,b,warehouse):   
    (ax,ay) = a
    (bx,by) = b
    # dprint(f"Swap {a} ({warehouse[ay][ax]}) <-> {b} ({warehouse[by][bx]})") 
    temp = warehouse[by][bx]
    warehouse[by][bx] = warehouse[ay][ax]
    warehouse[ay][ax] = temp
    # if debug:
    #     print_grid(warehouse)

def move_robot(m,robot_pos,warehouse):
    (nx,ny) = next_pos(robot_pos,m)    
    if warehouse[ny][nx] == ".":
        # easy case first
        swap( (robot_pos), (nx,ny), warehouse)
        robot_pos = (nx,ny)
    elif warehouse[ny][nx] == 'O':
        # dprint(f" move_robot {robot_pos} {m} : {warehouse[ny][nx]}")
        if( can_move(m,(nx,ny),warehouse)):
            move(m,(nx,ny),warehouse)
            swap( (robot_pos), (nx,ny), warehouse)
            return (nx,ny)
    return robot_pos

def print_grid(grid):
    for line in grid:
        print(''.join([str (i) for i in line]))

def find_crates(warehouse):
    crates = []
    for y in range(len(warehouse)):
        for x in range(len(warehouse[0])):
            if warehouse[y][x] == "O":
                crates.append((x,y))
    return crates

if __name__ == '__main__':
    button_costs = [3,1]
    print(f"*** Day 15, Part 1 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True

    warehouse,moves = read_data_file(sys.argv[1])
    dprint(f"Warehouse: {len(warehouse[0])} x {len(warehouse)})")
    robot_pos = find_robot(warehouse)
    dprint(f"Robot: {robot_pos}")
    # print_grid(warehouse)    
    for m in moves:
        dprint(f"Move: {m}, robot: {robot_pos}")
        robot_pos = move_robot(m,robot_pos,warehouse)
        if debug:
            print_grid(warehouse)

    print_grid(warehouse)

    gps_total = 0     
    crates = find_crates(warehouse)
    for c in crates:
        (x,y) = c
        gps_total += (100*y + x)

    print(f"Total of crate GPS values: {gps_total}")