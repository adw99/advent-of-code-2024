import sys
from collections import defaultdict

debug = False

def dprint(fs):
    if debug:
        print(fs)

def read_data_file(fname):
    df = open(fname, "r")
    lines = df.read().splitlines()
    starters = [ int(l) for l in lines]
    return starters

def mix_and_prune(i,i2):
    i3 = i ^ i2
    return i3 % 16777216

def gen_key(diffs,i):
    key = str(diffs[i-3]) + str(diffs[i-2]) + str(diffs[i-1]) + str(diffs[i])
    return key

if __name__ == '__main__':
    button_costs = [3,1]
    print(f"*** Day 22, Part 2 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    fname = sys.argv[1] if len(sys.argv) >=2 else 'sample.txt' 
    starters = read_data_file(fname)

    total = 0
    reps = 2000
    maps = []
    for s in starters:
        val_map = defaultdict(int)
        maps.append(val_map)
        diffs = []
        start = s
        prev = s % 10
        bids = [ prev ]
        for i in range(reps):
            s = mix_and_prune(s,s*64)
            s = mix_and_prune(s,int(s/32))
            s = mix_and_prune(s,s*2048)
            # dprint(f"{i}): {s}")
            new_bid = s%10
            bids.append(new_bid)
            df = new_bid - prev
            diffs.append(df)
            if i >= 3:
                key = gen_key(diffs,i)
                if val_map[key] == 0:
                    val_map[key] = new_bid
            prev = new_bid
    print("Maps created")
    key_max = 0
    best_key = ''
    for a in range(-9,9):
        for b in range(-9,9):
            for c in range(-9,9):
                for d in range(-9,9):
                    key = str(a) + str(b) + str(c) + str(d)
                    total = 0
                    for m in maps:
                        total += m[key]
                    if total>key_max:
                        best_key = key
                        key_max = total
    print(f"Max value found: {key_max} after {best_key}")
