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
        moves = ''
        keys = list(input)
        mpos = (2,0)
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
                dprint(f"moa->{moa}")
                movesa,mposa = move_encoder(moa,lookahead,mpos)
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
                dprint(f"mob->{mob}")
                movesb,mposb = move_encoder(mob,lookahead,mpos)
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

def move_encoder(input,depth,start):
    keypad = dirkeys
    result = ''
    avoid = keypad['AVOID']
    (sx,sy) = start
    for kl in list(input):
        target = keypad[kl]
        (tx,ty) = target
        xkey = ('<',-1) if (sx-tx)>0 else ('>',1)
        ykey = ('^',-1) if (sy-ty)>0 else ('v',1)
        # dprint(f"mpad ({sx},{sy}) => ({tx},{ty}))....{xkey},{ykey}")
        
        movesa = ''
        movesb = ''
        #plan a - horizontal first
        movax = movex((sx,sy),(tx,ty),xkey,avoid)
        movay = movey((tx,sy),(tx,ty),ykey,avoid)
        scorea = -1
        if movax == None or movay == None:
            # dprint(f"plan a bad moves: {movax} or {movay}")
            scorea = math.inf
        else:
            movesa = movax + movay + 'A'
            if depth>0:
                movesa,_ = move_encoder(movesa,depth-1,(2,0))
            scorea = len(movesa)

        #plan b - vertical first
        movby = movey((sx,sy),(tx,ty),ykey,avoid)
        movbx = movex((sx,ty),(tx,ty),xkey,avoid)
        scoreb = -1
        if movbx == None or movby == None:
            # dprint(f"plan b bad moves: {movby} or {movbx}")
            scoreb = math.inf
        else:
            movesb = movby + movbx + 'A'            
            if depth>0:
                movesb,_ = move_encoder(movesb,depth-1,(2,0))
            scoreb = len(movesb)
        # if movesa != movesb and (scorea + scoreb) != math.inf:
        #     print(f"Moves: {movesa} ({scorea}) vs {movesb} ({scoreb})")
        sx = tx
        sy = ty
        if( scorea != scoreb) and scorea != math.inf and scoreb != math.inf:
            dprint(f">>>>>> Scores: {scorea} vs {scoreb}")
        # if scorea == math.inf and scoreb == math.inf:
        #     dprint("*** Two impossible moves - should not happen")
        #     raise ValueError
        temp = movesa if scorea<=scoreb else movesb
        # dprint(f"encod {kl}{start} ==> {temp}")
        result += temp
    # if depth == 0:
    #     print(f"encoder({depth}): ({input}) => {result}")

    return result,(sx,sy)


def single_move_encoder(s,t): 
    (sx,sy) = dirkeys[s]
    (tx,ty) = dirkeys[t]

    deltax = sx - tx
    deltay = sy - ty
    xkey = ('<',-1) if deltax>0 else ('>',1)
    ykey = ('^',-1) if deltay>0 else ('v',1)
    dprint(f"({sx},{sy}) => ({tx},{ty}))....{xkey},{ykey}")

    #plan a - horizontal first
    movax = movex((sx,sy),(tx,ty),xkey,dirkeys['AVOID'])
    movay = movey((tx,sy),(tx,ty),ykey,dirkeys['AVOID'])
    scorea = -1
    if movax == None or movay == None:
        dprint(f"plan a bad moves: {movax} or {movay}")
        scorea = math.inf
    else:
        moa = movax + movay + 'A'
        dprint(f"moa->{moa}")
        movesa,_ = move_encoder(moa,lookahead,(2,0))
        scorea = len(movesa) if movesa != None else math.inf
    #plan b - vertical first
    movby = movey((sx,sy),(tx,ty),ykey,dirkeys['AVOID'])
    movbx = movex((sx,ty),(tx,ty),xkey,dirkeys['AVOID'])
    scoreb = -1
    if movbx == None or movby == None:
        dprint(f"plan b bad moves: {movby} or {movbx}")
        scoreb = math.inf
    else:
        mob = movby + movbx + 'A'            
        dprint(f"mob->{mob}")
        movesb,_ = move_encoder(mob,lookahead,(2,0))
        scoreb = len(movesb) if movesb != None else math.inf

    if scorea == math.inf and scoreb == math.inf:
        dprint("*** Two impossible moves - should not happen")
        raise ValueError

    if( scorea != scoreb) and scorea != math.inf and scoreb != math.inf:
        print(f"nnnnn Scores: {scorea} vs {scoreb} - {s} -> {t}")

    if scorea <= scoreb:
        return moa
    else:
        return mob



@functools.lru_cache(maxsize=10240)
def get_length(inp, depth ): 
    # print(f"gl>{inp} - {depth}")
    global move_cache
    if depth == 0: 
        return len(inp)
    prev = 'A'
    total_length = 0
    for char in inp:
        total_length += get_length(move_cache[(prev, char)], depth - 1) 
        prev = char
    return total_length

def solve_for_keys(depth,input):
    global numkeys

    numpad = Keypad(numkeys)
    moves = numpad.enter(input)
    print(f"Keypad.enter({input}): {moves}")

    move_length = get_length(moves,depth)
    return move_length

move_cache = {}
lookahead = 3

if __name__ == '__main__':
    print(f"*** Day 21 Part 1 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    fname = 'sample.txt' if len(sys.argv)<2 else sys.argv[1]
    inputs = read_data_file(fname)

    dk = dirkeys.keys()
    # def single_move_encoder(s,t)
    for i in dk:
        for j in dk:
            if i != 'AVOID' and j != 'AVOID':
                m = single_move_encoder(i,j)
                move_cache[(i,j)] = m
                print(f"* {i} -> {j}: {m}")

    movement_depth = 25
    total = 0

    for i in inputs:
        (keys,value) = i
        # dprint(f"> {keys} \n")
        solution = solve_for_keys(movement_depth, keys)
        print(f"{keys}: {solution}\n")
        print(f"{value} * {solution} = {solution * value}")
        total += solution * value

    print(f"Total complexity score: {total}")