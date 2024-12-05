import sys
import math

xword = "MAS"
rows = 0
cols = 0
debug = False

def read_data_file(fname):
    df = open(fname, "r")
    fs = df.read()
    return fs.split('\n')

def dprint(fs):
    if debug:
        print(fs)

def map_add(map,key,item):
    if( key not in map ):
        map[key] = [item]
    else:
        map[key].append(item)

def extract_rules(lines):
    rules = []
    rule_map = dict()
    for l in lines:
        if( '|' in l ):
            before = int(l[0:2])
            after = int(l[-2:])
            dprint(f"Line: {l} : {before}|{after}")
            rule = (before,after)
            rules.append(rule)
            map_add(rule_map,before,rule)
            map_add(rule_map,after,rule)
    return rules,rule_map

def extract_updates(lines):
    samples = []
    for l in lines:
        if( ',' in l):
            samples.append([int(i) for i in l.split(',')])
    return samples

def validate_rule(update, rule):
    before,after = rule
    if before in update and after in update:
        if update.index(before) >= update.index(after):
            return False
    return True

def validate_update(update, rule_map):
    result = True
    for page in update:
        pr = []
        if page in rule_map:
            pr = rule_map[page]
        for rule in pr:
            if not validate_rule(update,rule):
                dprint(f"Validation fail: {rule}, {update}")
                return False
    return result

def sort_rules(prs,porder):
    moves = 0
    for rule in prs:
        (before,after) = rule
        if before in porder and after in porder:
            if( porder[before] >= porder[after] ):
                moves += 1
                dprint(f"Moving {after} behind {before}")
                porder[after] = porder[before] + 1
    dprint(f"sort_rules, moves: {moves}")
    return porder,moves

def sort_update(up,rule_map):
    porder = {}
    prs = []
    for page in up:
        porder[page] = up.index(page) * 100
        prs += rule_map[page] if page in rule_map else []

    moves = 1
    limit = 100
    while moves>0 and limit>0:
        porder,moves = sort_rules(prs,porder)
        limit -= 1
    if limit == 0:
        print("*** WARNING: 100 sort limit reached")
    resorted = [i[0] for i in sorted(porder.items(), key=lambda item: item[1])]
    if debug:
        if not validate_update(resorted,rule_map):
            dprint(f"Resorted list fails validation? {up} -> {resorted}")
    return resorted,100-limit


if __name__ == '__main__':
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    lines = read_data_file(sys.argv[1])
    rules, rule_map = extract_rules(lines)
    updates = extract_updates(lines)
    dprint(f"Rules: {rule_map}")
    dprint(f"Updates: {updates}")
    
    total = 0
    count = 0
    max_sorts = 0
    for r in range(len(updates)):
        up = updates[r]
        result = validate_update(up, rule_map)
        dprint(f"Update {r}: {result} / {up}")
        if not result:
            fixed, sorts = sort_update(up, rule_map)
            count += 1
            if sorts > max_sorts:
                max_sorts = sorts
            total += fixed[math.floor(len(fixed)/2)]

    print(f"Final count: {total}, resorts: {count}, most sort loops: {max_sorts}")