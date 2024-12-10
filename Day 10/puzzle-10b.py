import sys
import itertools
import time

rows = 0
cols = 0
debug = False

def dprint(fs):
    if debug:
        print(fs)

def read_data_file(fname):
    global rows
    global cols
    df = open(fname, "r")
    fs = df.read()
    lines = fs.split('\n')
    grid = []
    # doing this so I can run the 'sparse' samples from the instructions
    rsi = lambda r: int(r) if '0' <= r <= '9' else -1
    for l in lines:
        grid.append( [rsi(r) for r in l])
    return grid

def find_zeroes(grid):
    zeroes = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == 0:
                zeroes.append((x,y))
    return zeroes

def valid(posx,posy):
    global rows
    global cols
    return  0 <= posx <= (cols-1) and 0 < posy <= (rows-1)

def next_steps(grid, posx, posy, path):
    global rows
    global cols
    n_steps = []
    value = grid[posy][posx]
    possible_directions = [(1,0), (-1,0), (0,1), (0,-1)]
    for d in possible_directions:
        (incx,incy) = d
        newx = posx + incx
        newy = posy + incy
        if (0 <= newx <= (cols-1)) and (0 <= newy <= (rows-1)):
            # dprint(f"> ({newx},{newy}): {grid[newy][newx]}")
            if grid[newy][newx] - grid[posy][posx] == 1:
                new_path = path.copy()
                new_path.append( (newx,newy))
                n_steps.append( (newx,newy,grid[newy][newx],new_path))
    # dprint(f"point({posx},{posy}) has next steps: {n_steps}")
    return n_steps


def find_trails(grid,start):
    trails = 0
    (startx,starty) = start
    paths = []
    options = next_steps(grid,startx,starty,[start])
    while len(options) >0:
        (newx,newy,value,path) = options.pop()
        if value == 9:
            if not path in paths:
                paths.append(path)
                trails +=1
        else:
            options += next_steps(grid,newx,newy,path)

    return trails,paths

if __name__ == '__main__':
    print(f"*** Day 10, Part 2 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    grid = read_data_file(sys.argv[1])
    rows = len(grid)
    cols = len(grid[0])
    dprint(f"Rows: {rows}, Cols: {cols}")
    zeroes = find_zeroes(grid)
    dprint(f"Zeroes found: {len(zeroes)}")

    total = 0
    for zero in zeroes:
        zt, paths = find_trails(grid,zero)
        dprint(f"Zero({zero}), trails: {zt}")
        total += zt

    print(f"Total trails found: {total}")