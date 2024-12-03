import re
import sys

def read_data_file(fname):
    df = open(fname, "r")
    return df.read()

def process_data_string(ds):
    rex = re.compile('mul\\((\d*)[,](\d*)\\)')
    tupe_list = rex.findall(ds)
    int_list = []
    for (a,b) in tupe_list:
        int_list.append( (int(a), int(b)))    
    return int_list

if __name__ == '__main__':
    tx = read_data_file(sys.argv[1])
    muls = process_data_string(tx)
    print(f"muls: {len(muls)}")
    sum = 0
    for (a,b) in muls:
        sum += a*b
    print(f"Total sum: {sum}")
