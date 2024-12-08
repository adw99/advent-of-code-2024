import sys
import itertools
import time

rows = 0
cols = 0
debug = False

def dprint(fs):
    if debug:
        print(fs)

def map_put(map,key,value):
    if key not in map:
        map[key] = [value]
    else:
        map[key].append(value)

def read_data_file(fname):
    global rows
    global cols

    df = open(fname, "r")
    fs = df.read()
    lines = fs.split('\n')
    rows = len(lines)
    cols = len(lines[0])
    grid = []
    antenna_list = {}
    count = 0
    for y in range(len(lines)):
        row = list(lines[y])
        grid.append(row)
        for x in range(len(row)):
            if( row[x] != '.'):
                map_put(antenna_list,row[x],(x,y))
                count += 1
    dprint(f"Rows: {rows}, cols: {cols}, antenna: {count}")
    return grid, antenna_list

def inrange(x,y):
    global rows
    global cols
    return (0 <= x < cols) and (0 <= y < rows)

def antinode(a1,a2,alist):
    x1 = a1[0] + ( a1[0]-a2[0] )
    y1 = a1[1] + ( a1[1]-a2[1] )
    if inrange(x1,y1) and not (x1,y1) in alist:  
        alist.append((x1,y1))

if __name__ == '__main__':
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    grid, antenna_list = read_data_file(sys.argv[1])
    start = time.time()
    dprint(f"Antenna list: {antenna_list}")
    anl = []
    for key in antenna_list.keys():
        ants = antenna_list[key]
        comb_list = itertools.product(ants, repeat=2)
        for c in comb_list:
            (a1,a2) = c
            if a1 != a2:
                antinode(a1,a2,anl)
                antinode(a2,a1,anl)
    total = len(anl)

    end = time.time()

    print(f"Antinodes found: {total}")
    print(f"Elapsed time: {end-start} (s)")
    dprint(f"Antinode list: {anl}")
