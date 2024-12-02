def read_data_file(fname):
    df = open(fname, "r")
    tx = df.read()

    return tx

def process_data_string(tx):
    lines = tx.split("\n")
    print(len(lines))

    la = []
    lb = []

    for l in lines:
        al = l.split()
        la.append(int(al[0]))
        lb.append(int(al[1]))

    return la,lb

if __name__ == '__main__':
    tx = read_data_file('puzzle-1-a.txt')
    la, lb = process_data_string(tx)
    la.sort()
    lb.sort()

    sum = 0
    for point in la:
        pc = lb.count(point)
        sum = sum + (point * pc)
    
    print(sum)