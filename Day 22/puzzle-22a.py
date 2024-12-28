import sys

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

if __name__ == '__main__':
    button_costs = [3,1]
    print(f"*** Day 22, Part 1 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    fname = sys.argv[1] if len(sys.argv) >=2 else 'sample.txt' 
    starters = read_data_file(fname)

    total = 0
    for s in starters:
        start = s
        # dprint(f"\n> {s}")
        for i in range(2000):
            s = mix_and_prune(s,s*64)
            s = mix_and_prune(s,int(s/32))
            s = mix_and_prune(s,s*2048)
            # dprint(f"{i}): {s}")
        dprint(f"{start} (2000) = {s}")
        total += s
    print(f"Total of 2000th secrets: {total}")