from collections import Counter

def read_data_file(fname):
    df = open(fname, "r")
    tx = df.read()

    return tx

def process_data_string(tx):
    lines = tx.split("\n")

    la = []
    lb = []

    for l in lines:
        al = l.split()
        la.append(int(al[0]))
        lb.append(int(al[1]))
    la.sort()
    lb.sort()
    return la,lb

def total(la,lb):
    lbc = Counter(lb)
    sum = 0
    for point in la:
        sum += (point * lbc[point])
    return sum

if __name__ == '__main__':
    tx = read_data_file('aoc-input-1.txt')
    la, lb = process_data_string(tx)
   
    print(f"Total: {total(la,lb)}")