import sys
import itertools
import time

rows = 0
debug = False
operations = ["+", "*"]

def dprint(fs):
    if debug:
        print(fs)

def read_data_file(fname):
    df = open(fname, "r")
    fs = df.read()
    lines = fs.split('\n')
    grid = []
    for l in lines:
        first = l.split(':')
        grid.append( ( int(first[0]), [int(i) for i in first[1].split()]))
    rows = len(grid)
    dprint(f"Rows: {rows}")
    return grid

def calc_val_option(num_list,op_list):
    total = num_list[0]
    for x in range(len(num_list)):
        if x > 0:
            op = op_list[x-1]
            if op == "+":
                total = total + num_list[x]
            elif op == "*":
                total = total * num_list[x]
            else:
                print(f"*** UNEXPECTED OPERATOR: {op}")
    return total

def validate_calibration(checksum,num_list):
    op_count = len(num_list) - 1
    op_list = itertools.product(operations, repeat=op_count)
    for ops in op_list:
        if calc_val_option(num_list,ops) == checksum:
            dprint(f"Numbers {num_list} with ops {ops} = {checksum}")
            return True
    return False

if __name__ == '__main__':
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    grid = read_data_file(sys.argv[1])
    start = time.time()
    dprint(f"First row: {grid[0]}")
    total = 0
    count = 0
    for line in grid:
        (checksum, num_list) = line
        if( validate_calibration(checksum,num_list)):
            count += 1
            total += checksum
    end = time.time()

    print(f"Total : {total}, success: {count} out of {len(grid)}")
    print(f"Elapsed time: {end-start} (s)")
