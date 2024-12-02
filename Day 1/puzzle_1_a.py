
def read_data_file(fname):
    df = open(fname, "r")
    return df.read()

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

def abs_sum(la,lb):
    return sum([abs(la[x]-lb[x]) for x in range(len(la)) ])

if __name__ == '__main__':
    tx = read_data_file('puzzle-1.txt')
    la, lb = process_data_string(tx)

    print(f"Sum: {abs_sum(la,lb)}")
