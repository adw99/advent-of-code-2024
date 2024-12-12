import sys
from enum import Enum


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
    for l in lines:
        grid.append( [r for r in l])
    rows = len(grid)
    cols = len(grid[0])
    return grid

direction_options = [(1,0,"LEFT"),(-1,0,"RIGHT"),(0,1,"DOWN"),(0,-1,"UP")]

def in_bounds(x,y):
    global rows
    global cols
    return ( 0 <= x <= (cols-1) and 0 <= y <= (rows-1))

def find_region(grid,x,y):
    global direction_options
    region = [(x,y)]
    plant_type = grid[y][x]    
    stack = [(x,y)]
    while len(stack) > 0:
        (px,py) = stack.pop()
        for (xacc,yacc,side) in direction_options:             
            newx = px + xacc
            newy = py + yacc
            if in_bounds(newx,newy) and (newx,newy) not in region:
             if grid[newy][newx] == plant_type:
                region.append((newx,newy))
                stack.append((newx,newy))                
    return region

def map_put(dmap,key,value):
    if key not in dmap:
        dmap[key] = [value]
    else:
        dmap[key].append(value)


def edge_list_to_map(elist,key_index,val_index):
    dmap = {}
    for e in elist:
        map_put(dmap, e[key_index], e[val_index])
    return dmap

def count_sides(dmap):
    sides = 0

    for key in dmap.keys():
        plist = dmap[key]
        if len(plist) == 1:
            sides += 1
        else:
            # we need to sort the list and see how many edges it represents
            plist.sort()
            pcount = 0
            prev = -5 # bogus starting point
            for pt in plist:
                if abs(pt-prev) != 1:
                    pcount +=1
                prev = pt
            sides += pcount

    return sides

def find_sides(plant_type,region):
    global direction_options
    count = 0
    edges = [[],[],[],[]]
    y_indexes = { -1: 0, 1:1}
    x_indexes = {-1: 2, 1:3}
    for (px,py) in region:
        for (xacc,yacc,side) in direction_options:
            newx = px + xacc
            newy = py + yacc
            if not in_bounds(newx,newy) or grid[newy][newx] != plant_type:
                # this is an edge of the region, add it to the appropriate list
                # we have 4 lists, for horizontal-top, horizontal-bottom, 
                # vertical-left and vertical-right
                if yacc != 0:                    
                    edges[y_indexes[yacc]].append((newx,newy))
                else:
                    edges[x_indexes[xacc]].append((newx,newy))

    # convert edge lists to maps
    count += count_sides(edge_list_to_map(edges[0],1,0))
    count += count_sides(edge_list_to_map(edges[1],1,0))
    count += count_sides(edge_list_to_map(edges[2],0,1))
    count += count_sides(edge_list_to_map(edges[3],0,1))

    return count

if __name__ == '__main__':
    bottoms = []
    print(f"*** Day 12, Part 2 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True

    grid = read_data_file(sys.argv[1])
    dprint(f"Rows({rows}), cols: {cols} \n {grid}")

    processed = []
    regions = []

    # Identify plant regions
    for y in range(len(grid[0])):
        for x in range(len(grid[0])):
            if (x,y) not in processed:
                plant_type = grid[y][x]
                new_region = find_region(grid,x,y)
                dprint(f"Region found: {plant_type}, size={len(new_region)}")
                processed += new_region
                regions.append( (plant_type,new_region))

    total = 0
    for reg in regions:
        (plant_type,points) = reg
        sides = find_sides(plant_type,points)
        dprint(f"Sides {plant_type}: {sides}")
        total += sides * len(points)

    print(f"Total fencing cost = {total}")
