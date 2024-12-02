
def read_data_file(fname):
    df = open(fname, "r")
    tx = df.read()

    return tx

def process_data_string(tx):
    lines = tx.split("\n")
    print(len(lines))

    reports = []

    for l in lines:
        sl = l.split()
        reports.append([int(i) for i in sl])

    print(f"{type(reports)} / {len(reports)}")
    return reports

def process_report(r):
    increasing = False
    direction_found = False
    for rd in range(len(r)):
        if( rd > 0 ):
            #establishing direction
            if not direction_found and r[rd] != r[rd-1]:
                increasing = ( r[rd] > r[rd-1] )
                direction_found = True
                # print(f"Increasing ? {increasing} : {r}")
            #check diff
            diff = abs(r[rd] - r[rd-1])
            if( diff < 1 or diff > 3):
                print(f"Invalid change: {r}")
                return False
            # check directionality
            if( increasing and r[rd] < r[rd-1]) or ( not increasing and r[rd] > r[rd-1]):
                print(f"Invalid direction: {r}")
                return False
            
    return True


if __name__ == '__main__':
    tx = read_data_file('puzzle-2.txt')
    reports = process_data_string(tx)

    safe = 0
    for r in reports:
        if process_report(r):
            safe += 1

    print(f"Reports: {len(reports)}, safe reports: {safe}")