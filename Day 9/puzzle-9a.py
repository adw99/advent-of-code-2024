import sys
import itertools
import time

debug = False

def dprint(fs):
    if debug:
        print(fs)

def read_data_file(fname):
    df = open(fname, "r")
    fs = df.read()
    dlist = list(fs)
    # dprint(f"separated list: {dlist}")
    blocklist = []
    blocknumber = 0
    for i in range(len(dlist)):
        count = int(dlist[i])
        if i % 2 == 0:
            # even numbered entries are data
            new_block  = [blocknumber] * count
            # dprint(f"Adding new block: {new_block}")
            blocklist += [blocknumber] * count
            blocknumber += 1
        else:
            # odd numbered entries are spaces
            spacelist = ['.'] * count
            blocklist += spacelist

    return blocklist

if __name__ == '__main__':
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    block_list = read_data_file(sys.argv[1])
    # dprint(f"{block_list}")

    # 'Defragment' the 'disk
    dprint(f"Initial block list length: {len(block_list)}")

    index = 0
    back_index = len(block_list)-1
    keep_going = True
    while keep_going:
        if block_list[index] == '.':
            moved = '.'
            while moved == '.':
                moved = block_list[back_index]
                back_index -=1
            # dprint(f"Moving {moved}")
            block_list[index] = moved
            block_list[back_index+1] = '.'
        index += 1
        keep_going = index < back_index

    dprint(f"Final block list length: {len(block_list)}")
    # dprint(f"Final block list: {block_list}")

    #calculate checksum
    checksum = 0
    for i in range(len(block_list)):
        if block_list[i] != '.':
            checksum += i*block_list[i]

    print(f"Final checksum: {checksum}")