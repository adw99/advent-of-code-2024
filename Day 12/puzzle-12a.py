import sys


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

direction_options = [(1,0),(-1,0),(0,1),(0,-1)]

def in_bounds(x,y):
    global rows
    global cols
    return ( 0 <= x <= (cols-1) and 0 <= y <= (rows-1))

def find_region(grid,x,y):
    global direction_options
    region = [(x,y)]
    plant_type = grid[y][x]    
    stack = [(x,y)]
    # dprint(f"find_region({x},{y},{plant_type})")
    while len(stack) > 0:
        (px,py) = stack.pop()
        for (xacc,yacc) in direction_options:             
            newx = px + xacc
            newy = py + yacc
            if in_bounds(newx,newy) and (newx,newy) not in region:
             if grid[newy][newx] == plant_type:
                region.append((newx,newy))
                stack.append((newx,newy))                
    return region

def find_perimeter(plant_type,region):
    global direction_options
    count = 0

    for (px,py) in region:
        for (xacc,yacc) in direction_options:
            newx = px + xacc
            newy = py + yacc
            if not in_bounds(newx,newy) or grid[newy][newx] != plant_type:
                count +=1        

    return count

if __name__ == '__main__':
    bottoms = []
    print(f"*** Day 12, Part 1 ***\n")
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
        per = find_perimeter(plant_type,points)
        dprint(f"Perimiter {plant_type}: {per}")
        total += per * len(points)

    print(f"Total fencing cost = {total}")
