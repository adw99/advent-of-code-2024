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
    if debug:
        output = ""
        stone = list
        while not stone == None:
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
    while stone != None:
        val = stone.value
        strv = str(stone.value)
        # dprint(f">> {val} / {strv} - {len(strv)} / {len(strv) %2}")
        if stone.value == 0:
            stone.value = 1
            # dprint(f"|| Flipped zero to 1")
        elif len(strv) % 2 == 0:
            half = int(len(strv)/2)
            # dprint(f"|| spliting'{strv}' in half ({half})")
            left_val = int(strv[:half])
            right_val = int(strv[half:])
            new_stone = Stone(right_val,stone,stone.next)
            stone.next = new_stone
            stone.value = left_val            
            # Move the index ahead so as to immediately process the stone we just added
            stone = new_stone 
            # dprint(f" next up: {stone.next}")
        else:
            # dprint(f"|| multiplying {stone.value} * 2048")
            stone.value = stone.value * 2024
        
        # dprint(f"Avancing pointer to {stone.value}")
        stone = stone.next


if __name__ == '__main__':
    print(f"*** Day 11, Part 1 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    start = read_data_file(sys.argv[1])
    stone_list = build_list(start)
    print_stone_list(stone_list)

    for i in range(25):
        blink(stone_list)
        dprint(f"?? {i}: {print_stone_list(stone_list)}")
        
    print(f"Final list length: {list_length(stone_list)}")


