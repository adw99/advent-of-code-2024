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
        if update.index(before) > update.index(after):
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
                return False
    return result

if __name__ == '__main__':
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    lines = read_data_file(sys.argv[1])
    rules, rule_map = extract_rules(lines)
    updates = extract_updates(lines)
    dprint(f"Rules: {rule_map}")
    dprint(f"Updates: {updates}")
    
    count = 0
    for r in range(len(updates)):
        up = updates[r]
        result = validate_update(up, rule_map)
        dprint(f"Update {r}: {result} / {up}")
        if result:
            count += up[math.floor(len(up)/2)]

    print(f"Final count: {count}")