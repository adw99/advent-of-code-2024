import re
import sys

def read_data_file(fname):
    df = open(fname, "r")
    return df.read()

def process_data_string(ds_in):
    # hard code do() start and don't() end
    # easier to parse if we know all blocks have a do() start and don't() end
    ds = "do()" + ds_in + "don't()"
    mul_rex = re.compile('mul\\((\d*)[,](\d*)\\)')
    # key bit - had to include line return in the capture,
    # otherwise it didn't work, even with the multiline flag on
    do_blocks_rex = re.compile('do\(\)((?:.|\n)*?)don\'t\(\)')   
    blocks = do_blocks_rex.findall(ds)
    print(f"Total blocks: {len(blocks)}")
    tupe_list = []
    for b in blocks:
        tupe_list += mul_rex.findall(b)
    return tupe_list

if __name__ == '__main__':
    tx = read_data_file(sys.argv[1])
    muls = process_data_string(tx)
    print(f"muls: {len(muls)}")
    sum = 0
    for (a,b) in muls:
        sum += int(a)*int(b)
    print(f"Total sum: {sum}")
