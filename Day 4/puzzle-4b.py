import sys

xword = "MAS"
rows = 0
cols = 0
debug = False

def read_data_file(fname):
    df = open(fname, "r")
    return df.read()

def process_data_string(ds):
    lines = ds.split('\n')
    grid = []
    for l in lines:
        grid.append(list(l))

    return grid


def process_loc(grid,loc):
    (y,x) = loc
    combinations = ["MS", "SM"]
    # ignore a's on the 'edge' of the grid
    if( x>0 and x<cols-1 and y>0 and y<rows-1 ):
        c1 = grid[y+1][x+1] + grid[y-1][x-1]
        c2 = grid[y+1][x-1] + grid[y-1][x+1]

        return (c1 in combinations and c2 in combinations)
    return False

if __name__ == '__main__':
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    tx = read_data_file(sys.argv[1])
    grid = process_data_string(tx)
    rows = len(grid)
    cols = len(grid[0])
    print(f"Grid: {rows} / {cols}")
    xcount = 0
    acount = 0
    # Find all a's
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'A':
                acount += 1
                if process_loc(grid,(r,c)):
                    xcount += 1
                    if debug:
                        print(f"Loc ({r},{c}) matches")
    
    print(f"A's: {acount}")

    print(f"Xmas count: {xcount}")