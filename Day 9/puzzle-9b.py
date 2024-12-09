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
    data_list = []
    space_list = []
    blocknumber = 0
    for i in range(len(dlist)):
        count = int(dlist[i])
        if i % 2 == 0:
            # even numbered entries are data
            new_block  = [blocknumber] * count
            dprint(f"Adding new block: {new_block}, ({count}, {len(blocklist)})")
            data_list.append( (blocknumber,count, len(blocklist)))
            blocklist += new_block
            blocknumber += 1
        else:
            # odd numbered entries are spaces
            new_space = ['.'] * count
            dprint(f"Adding new space: {new_space}, ({count}, {len(blocklist)})")
            space_list.append( (count, len(blocklist)))
            blocklist += new_space

    return blocklist,data_list,space_list

def find_space_block(space_list,data_count):
    for i in range(len(space_list)):
        (space_count,index) = space_list[i]
        if space_count >= data_count:
            # dprint(f"Returning space {space_count}, {index}, {i}")
            return (space_count,index,i)
    return (-1,-1,-1)

def count_spaces(block_list):
    count = 0
    for i in range(len(block_list)):
        if block_list[i] == ".":
            count += 1

    return count

if __name__ == '__main__':
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    block_list,data_list,space_list = read_data_file(sys.argv[1])
    dprint(f"{block_list[0:25]}")

    # 'Defragment' the 'disk
    dprint(f"Initial block list length: {len(block_list)}, spaces: {count_spaces(block_list)}")
    moves = 0
    for i in reversed(range(len(data_list))):
        (blocknumber,count,data_block_index) = data_list[i]
        (space_count, space_block_index, space_index) = find_space_block(space_list, count)
        #only move the data block backwards
        if( space_count != -1 and space_block_index<data_block_index):
            # dprint(f"Found space block: {space_index}: {space_list[space_index]}")
            for i in range(count):
                block = block_list[data_block_index + i]
                dprint(f"Moving {block} from {data_block_index + i} to {space_block_index + i}")
                moves += 1
                block_list[data_block_index + i] = '.'
                block_list[space_block_index + i] = block
            (space_count,index) = space_list[space_index]
            space_list[space_index] = (space_count-count,index+count)
            # dprint(f"Updated space block: {space_index}: {space_list[space_index]}")


    dprint(f"Final block list length: {len(block_list)}, spaces: {count_spaces(block_list)}")
    dprint(f"Final block list: {block_list[0:25]}")
    dprint(f"Moves: {moves}")

    #calculate checksum
    checksum = 0
    for i in range(len(block_list)):
        if block_list[i] != '.':
            checksum += i*block_list[i]

    print(f"Final checksum: {checksum}")