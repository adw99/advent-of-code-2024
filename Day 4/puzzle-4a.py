import sys

xword = "XMAS"

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


def diagonal_slice(grid,r,c,vacc,hacc):
    wl = len(xword)
    rows = len(grid)
    cols = len(grid[0])
    chars = []
    if debug:
        print(f"Diag> {r},{c},{vacc},{hacc}")
    for inc in range(wl):
        y = r + (inc * vacc)
        x = c + (inc * hacc)

        if( x>=0 and y>=0 and x<rows and y<cols):
            if debug:
                print(f">> {inc}, {y}, {x}: {grid[y][x]}")
            chars.append(grid[y][x])
    word = ''.join(chars)
    if( debug and len(word) == wl):
        print(f">>> {word}")
    return ''.join(chars)                


def process_x(grid,co):
    rows = len(grid)
    cols = len(grid[0])
    (r,c) = co
    if debug:
        print(f"X({r},{c})")
    wl = len(xword)
    words = []
    if( cols-c >= wl ):
        # Check right
        words.append(''.join(grid[r][c:c+wl]))
    if( c >= (wl-1) ):
        # Check left
        words.append(''.join(reversed(grid[r][c-wl+1:c+1])))
    if( rows-r >= wl):
        #check down
        slice = [grid[i][c] for i in range(r,r+wl)]
        words.append(''.join(slice))
        if debug:
            print(f"Vertical down slice: {''.join(slice)}")
    if( r>= (wl-1)):
        #check up
        slice = [grid[i][c] for i in range(r-wl+1,r+1)]
        words.append(''.join(reversed(slice)))
        if debug:
            print(f"Vertical up slice: {''.join(reversed(slice))}")
    if debug:
        print(f"Word list defore diags: {words}")


    diags = []
    diags.append(diagonal_slice(grid,r,c,1,1))
    diags.append(diagonal_slice(grid,r,c,1,-1))
    diags.append(diagonal_slice(grid,r,c,-1,1))
    diags.append(diagonal_slice(grid,r,c,-1,-1))
    words += [diags[i] for i in range(len(diags)) if len(diags[i])==wl]

    if( debug and len(diags)> 0):
        print(f"Diagonals({r},{c}): {[diags[i] for i in range(len(diags)) if len(diags[i])==wl]}")
    if debug:
        print(f"Word list: {words}")
    count = 0
    for w in words:
        if w == xword:
            count += 1


    if debug:
        print(f"X({r},{c}): {count}")
    return count

if __name__ == '__main__':
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    tx = read_data_file(sys.argv[1])
    grid = process_data_string(tx)
    rows = len(grid)
    cols = len(grid[0])
    print(f"Grid: {rows} / {cols}")
    xlist = []
    # Find all x's
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'X':
                xlist.append( (r,c) )
    
    print(f"X's: {len(xlist)}")

    xcount = 0
    for xco in xlist:
        xcount += process_x(grid,xco)
    # xcount += process_x(grid,(3,9))

    print(f"Xmas count: {xcount}")