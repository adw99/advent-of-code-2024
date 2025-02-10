import sys
import re
import math
import functools

debug = False

def dprint(fs):
    if debug:
        print(fs)

def read_data_file(fname):
    rex = re.compile("(\\d*)")
    
    df = open(fname, "r")
    lines = df.read().splitlines()
    inputs = []
    for l in lines:
        m = rex.search(l)
        inputs.append( (l,int(m[1])) )

    return inputs

numkeys = {
    '7': (0,0),
    '8': (1,0),
    '9': (2,0),
    '4': (0,1),
    '5': (1,1),
    '6': (2,1),
    '1': (0,2),
    '2': (1,2),
    '3': (2,2),
    '0': (1,3),
    'A': (2,3),
    'AVOID': (0,3)
}

dirkeys = {
    '^': (1,0),
    'A': (2,0),
    '<': (0,1),
    'v': (1,1),
    '>': (2,1),
    'AVOID': (0,0)
}

class Keypad:
    def __init__(self,keypad):
        (self.x,self.y) = keypad['A']
        self.avoid = keypad['AVOID']
        (self.avoidx,self.avoidy) = self.avoid
        self.keypad = keypad
    def __str__(self):
        return f"({self.x},{self.y})"
    def check(self):
        return (self.x,self.y) != self.avoid


    def enter(self,input):
        global lookahead
        moves = ''
        keys = list(input)
        prev = 'A'
        dprint(f"AVOID: {self.avoid}")
        for k in keys:    
            dprint(f">>> {k}")        
            target = self.keypad[k]
            (tx,ty) = target
            (sx,sy) = (self.x,self.y)
            dprint(f"moving ({sx},{sy}) --> ({tx},{ty})")
            deltax = self.x - tx
            deltay = self.y - ty
            xkey = ('<',-1) if deltax>0 else ('>',1)
            ykey = ('^',-1) if deltay>0 else ('v',1)
            dprint(f"({sx},{sy}) => ({tx},{ty}))....{xkey},{ykey}")

            #plan a - horizontal first
            movax = movex((sx,sy),(tx,ty),xkey,self.avoid)
            movay = movey((tx,sy),(tx,ty),ykey,self.avoid)
            scorea = -1
            if movax == None or movay == None:
                dprint(f"plan a bad moves: {movax} or {movay}")
                scorea = math.inf
            else:
                moa = movax + movay + 'A'
                dprint(f"moa=={moa}")
                movesa,mposa = move_encoder(moa,prev,lookahead)
                scorea = len(movesa) if movesa != None else math.inf
                dprint(f"{k}-A {moa} --> {movesa} ({mposa}) / {scorea}")
            #plan b - vertical first
            movby = movey((sx,sy),(tx,ty),ykey,self.avoid)
            movbx = movex((sx,ty),(tx,ty),xkey,self.avoid)
            scoreb = -1
            if movbx == None or movby == None:
                dprint(f"plan b bad moves: {movby} or {movbx}")
                scoreb = math.inf
            else:
                mob = movby + movbx + 'A'            
                dprint(f"mob=={mob}")
                movesb,mposb = move_encoder(mob,prev,lookahead)
                scoreb = len(movesb) if movesb != None else math.inf
                dprint(f"{k}-B {mob} --> {movesb} ({mposb}) / {scoreb}")

            if scorea == math.inf and scoreb == math.inf:
                dprint("*** Two impossible moves - should not happen")
                raise ValueError

            if( scorea != scoreb) and scorea != math.inf and scoreb != math.inf:
                dprint(f"nnnnn Scores: {scorea} vs {scoreb} - {movesa} vs {movesb}")

            if scorea <= scoreb:
                moves += moa
                mpos = mposa
            else:
                moves += mob
                mpos = mposb
            self.x = tx
            self.y = ty
        dprint(f"Enter({input}) = {moves}")
        return moves            

def movex(start,target,xkey,avoid):
    moves = ''
    (sx,sy) = start
    (tx,_) = target
    while sx != tx:
        sx += xkey[1]
        moves += xkey[0]
        if(sx,sy) == avoid:
            return None
    # dprint(f"movex: {start}, {target}, {xkey} --> {moves}")    
    return moves

def movey(start,target,ykey,avoid):
    moves = ''
    (sx,sy) = start
    (_,ty) = target
    while sy != ty:
        sy += ykey[1]
        moves += ykey[0]
        if(sx,sy) == avoid:
            return None
    # dprint(f"movey: {start}, {target}, {ykey} --> {moves}")
    return moves


def move_size(input,prev,depth):
    moves = move_encoder(input,prev,depth)
    return len(moves) if moves != None else math.inf


def move_encoder(input,prev,depth):
    dprint(f"in>move_encoder({input},{prev},{depth})")
    start = dirkeys[prev]
    if depth == 0:
        return input,start
    moves = ''
    keys = 0
    keylist = list(input)
    prev2 = prev
    for key in keylist:
        keys += 1
        m = single_move_encoder_2(prev2,key,depth)
        dprint(f">>>> move_encoder({depth}): {key} ->  {m}")
        moves += m
        prev2 = key
    return moves,start


def single_move_encoder_2(prev,next,depth):
    (sx,sy) = dirkeys[prev]
    (tx,ty) = dirkeys[next]
    avoid = dirkeys['AVOID']
    xkey = ('<',-1) if (sx-tx)>0 else ('>',1)
    ykey = ('^',-1) if (sy-ty)>0 else ('v',1)

    movesa = ''
    movesb = ''
    #plan a - horizontal first
    movax = movex((sx,sy),(tx,ty),xkey,avoid)
    movay = movey((tx,sy),(tx,ty),ykey,avoid)
    scorea = -1
    if movax == None or movay == None:
        scorea = math.inf
    else:
        movesa = movax + movay + 'A'
        ma = move_encoder(movesa,'A',depth-1)
        scorea = len(ma)
        movesa = movax + movay + 'A'

    #plan b - vertical first
    movby = movey((sx,sy),(tx,ty),ykey,avoid)
    movbx = movex((sx,ty),(tx,ty),xkey,avoid)
    scoreb = -1
    if movbx == None or movby == None:
        scoreb = math.inf
    else:
        movesb = movby + movbx + 'A'    
        mb = move_encoder(movesb,'A',depth-1)
        scoreb = len(mb)
        movesb = movby + movbx + 'A'          
    sx = tx
    sy = ty
    if scorea == math.inf and scoreb == math.inf:
        raise ValueError(f"both paths are invalid: ({sx},{sy}): {movesa} / {movesb}")
    result = movesa if scorea<scoreb else movesb
    return result


@functools.lru_cache(maxsize=10240)
def get_length(input, depth ): 
    global move_cache
    if depth == 0: 
        return len(input)
    prev = 'A'
    total_length = 0
    for char in input:
        total_length += get_length(move_cache[(prev, char)], depth - 1) 
        prev = char
    return total_length

def solve_for_keys(depth,input):
    global numkeys

    numpad = Keypad(numkeys)
    moves = numpad.enter(input)
    dprint(f"Keypad.enter({input}): {moves}")

    move_length = get_length(moves,depth)

    dprint(f"d({input}): {move_length}")

    return move_length

lookahead = 8
move_cache = {}

if __name__ == '__main__':
    print(f"*** Day 21 Part 2 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    fname = 'sample.txt' if len(sys.argv)<2 else sys.argv[1]
    inputs = read_data_file(fname)

    movement_depth = 25
    total = 0

    dk = dirkeys.keys()
    for i in dk:
        for j in dk:
            if i != 'AVOID' and j != 'AVOID':
                move_cache[(i,j)] = single_move_encoder_2(i,j,lookahead)

    # result = solve_for_keys(movement_depth,'379A')
    # print(f"379A: {result} / {result * 379}")
    for i in inputs:
        (keys,value) = i
        # dprint(f"> {keys} \n")
        solution = solve_for_keys(movement_depth, keys)
        dprint(f"{keys}: {solution}\n")
        print(f"{value} * {solution} = {solution * value}")
        total += solution * value

    print(f"Total complexity score: {total}")
