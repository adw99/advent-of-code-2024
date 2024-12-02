import sys

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

    return reports

def process_report(r):
    increasing = False
    bd_count = 0
    diag = ""
    increasing = ( r[1] > r[0] )
    for rd in range(len(r)):
        bad_data = False
        if( rd > 0 ):
            #check diff
            diff = abs(r[rd] - r[rd-1])
            if( diff < 1 or diff > 3):
                diag += f"Invalid change: {r[rd]} - {r[rd-1]} "
                bad_data = True
            # check directionality
            elif( increasing and r[rd] < r[rd-1]) or ( not increasing and r[rd] > r[rd-1]):
                diag += f"Invalid direction: {r[rd]} - {r[rd-1]} "
                bad_data = True
        if( bad_data):
            bd_count += 1

    return True if bd_count==0 else False


if __name__ == '__main__':
    tx = read_data_file(sys.argv[1])
    reports = process_data_string(tx)

    safe = 0
    seconds = 0
    for r in reports:
        if process_report(r):
            safe += 1
        else:
            retry = False
            for i in range(len(r)):
                new_r = r[:i] + r[i+1:]
                if process_report(new_r):
                    print(f"Second chance: {r} / {new_r}")
                    safe += 1
                    seconds += 1
                    break


    print(f"Reports: {len(reports)}, safe reports: {safe}, worked on second chance: {seconds}")