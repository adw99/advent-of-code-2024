
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

    print(f"{la[0]} / {lb[0]}")
    print(f"{la[10]} / {lb[10]}")

    sum = 0
    for i in range(len(la)):
        diff = abs(la[i] - lb[i])
        print(f"{la[i]} - {lb[i]} = {diff}")
        sum = sum + diff

    print(f"Sum: {sum}")
