import sys
import re

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
        self.val = 'A'
    def __str__(self):
        return f"({self.x},{self.y})"
    def check(self):
        return (self.x,self.y) != self.avoid


    def enter(self,input):
        moves = ''
        keys = list(input)
        for k in keys:            
            target = self.keypad[k]
            m = self.move(target)
            self.val = k
            moves += m
        return moves            

    def movex(self,target,xkey):
        moves = ''
        (tx,_) = target
        while self.x != tx:
            self.x += xkey[1]
            moves += xkey[0]
            if not self.check():
                return None
        return moves
    def movey(self,target,ykey):
        moves = ''
        (_,ty) = target
        while self.y != ty:
            self.y += ykey[1]
            moves += ykey[0]
            if not self.check():
                return None
        return moves


    def move(self,target):
        moves = ''
        (tx,ty) = target
        deltax = self.x - tx
        deltay = self.y - ty
        # dprint(f"Delta ({deltax},{deltay})")
        xkey = ('<',-1) if deltax>0 else ('>',1)
        ykey = ('^',-1) if deltay>0 else ('v',1)
        # dprint(f"mkeys: {xkey} / {ykey}")
        xmoves = abs(deltax)
        ymoves = abs(deltay)
        if tx==self.avoidx:
            xmoves -=1
        if ty==self.avoidy:
            ymoves -=1
        if xmoves > ymoves:
            moves += self.movex(target,xkey)
            moves += self.movey(target,ykey)
        else:
            moves += self.movey(target,ykey)
            moves += self.movex(target,xkey)
        moves += 'A'
        return moves


def solve_for_keys(numpad,movepad,depth,input):
    curr = input
    curr = numpad.enter(input)
    for i in range(depth):
        curr = movepad.enter(curr)
        dprint(f"{input}: {curr}")
    return curr

if __name__ == '__main__':
    button_costs = [3,1]
    print(f"*** Day 17, Part 1 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    inputs = read_data_file(sys.argv[1])

    movement_depth = 2
    total = 0
    numpad = Keypad(numkeys)
    movepad = Keypad(dirkeys)

    # solution = solve_for_keys(numpad,pads,'379A')
    for i in inputs:
        (keys,value) = i
        solution = solve_for_keys(numpad, movepad, movement_depth, keys)
        print(f"{keys}: {solution}")
        print(f"{value} * {len(solution)} = {len(solution) * value}")
        total += len(solution) * value

    print(f"Total complexity score: {total}")