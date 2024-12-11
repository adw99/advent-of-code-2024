import sys
import time


rows = 0
cols = 0
debug = False

class Stone:
    def __init__(self,value,prev,next):
        self.value = value
        self.prev = prev
        self.next = next
    def __str__(self):
        return str(self.value)

def dprint(fs):
    if debug:
        print(fs)

def read_data_file(fname):
    global rows
    global cols
    df = open(fname, "r")
    fs = df.read()
    nums = fs.split()
    return [int(i) for i in nums]

def  build_list(num_list):
    # Build the doubly-linked list
    stone_list = None
    prev_stone = None
    for i in range(len(start)):        
        new_stone = Stone(start[i], prev_stone, None)
        if prev_stone != None:
            prev_stone.next = new_stone
        prev_stone = new_stone
        if i ==0:
            stone_list = new_stone
    return stone_list

def print_stone_list(list):
    output = ""
    stone = list
    while stone != None:
        if output != "":
            output += ","
        output += f"{stone.value}"
        stone = stone.next
    return output

def list_length(list):
    count = 0
    stone = list
    while not stone == None:
        count +=1
        stone = stone.next
    return count

def blink(stone_list):
    stone = stone_list
    dprint(f"^^ Blink: {stone.value} / {stone.next}")
    while stone != None:
        val = stone.value
        strv = str(stone.value)
        if stone.value == 0:
            stone.value = 1
        elif len(strv) % 2 == 0:
            half = int(len(strv)/2)
            left_val = int(strv[:half])
            right_val = int(strv[half:])
            new_stone = Stone(right_val,stone,stone.next)
            stone.next = new_stone
            stone.value = left_val            
            # Move the index ahead so as to immediately process the stone we just added
            stone = new_stone 
        else:
            stone.value = stone.value * 2024
        
        # dprint(f"Avancing pointer to {stone.value}")
        stone = stone.next

def cache_get(val,loops):
    global known_values
    key = f"v:{val}:{loops}"
    if key in known_values:
        return known_values[key]
    else:
        return None

def cache_put(val,loops,num):
    global known_values
    if loops>1:
        key = f"v:{val}:{loops}"
        known_values[key] = num


def count_one_stone(stone, loops):
    dprint(f"CC {stone.value}:{loops}")

    global bottoms
    cache = cache_get(stone.value,loops)
    if cache != None:
        return cache

    entry_values = (stone.value, loops)    
    loops_remaining = loops
    while stone.next == None and loops_remaining>0:
        loops_remaining -=1
        blink(stone)

    if loops_remaining == 0:
        # we reached the 'bottom', visualizing it as a binary tree
        length = list_length(stone)
        plist = print_stone_list(stone)
        dprint(f">> Bottom {stone.value}: {length} | {plist}")
        bottoms.append(stone.value)
        if( stone.next != None):
            snext = stone.next
            bottoms.append(snext.value)
        return length
    else:
        # our stone has split, so recurse
        left_stone = Stone(stone.value,None,None)
        left = count_one_stone(left_stone,loops_remaining)
        dprint(f"Left split ({left_stone.value}:{loops_remaining}): {left}")
        next_stone = stone.next
        right_stone = Stone(next_stone.value,None,None)
        right = count_one_stone(right_stone,loops_remaining)
        dprint(f"Right split ({right_stone.value}:{loops_remaining}): {right}")
        cache_put(entry_values[0], entry_values[1], left+right)
        return left + right

if __name__ == '__main__':
    bottoms = []
    print(f"*** Day 11, Part 1 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    loops = 25
    if(len(sys.argv) >=4):
        loops = int(sys.argv[3])
    print(f"LOOPS: {loops}")
    known_values = { "v:-1:25" : -1 } # for result caching, just seeding an invalid answer

    start_list = read_data_file(sys.argv[1])
    start = time.time_ns()
    interval = start
    count = 0
    known_values = { "-1": -1}
    for i in range(len(start_list)):
        stone = Stone( start_list[i], None, None)
        length = count_one_stone(stone,loops)
        print(f"{i}): ({start_list[i]}) {length} - { (time.time_ns()-interval)/1000000000} (s)")
        interval = time.time_ns()
        count += length
    end = time.time_ns()
    print(f"Final list length: {count}")
    print(f"Elapsed time {(end-start)/1000000000} (s)")
    print(f"Cached values: {len(known_values.keys())}")

    # stone = Stone(1,None,None)
    # length = count_one_stone(stone,loops)
    # print(f"Length(1:5) = {length}")
    # print(f"List: {bottoms}")
    # print(f"Length: {len(bottoms)}")
    dprint(f"Cache: {known_values}")
