import sys
from enum import Enum

debug = False

crate_bits = ['[',']']

class Crate:
    def __init__(self,lx,rx,y):
        global crate_bits
        self.lx = lx
        self.rx = rx
        self.y = y
        self.crate_bits = crate_bits
    def __str__(self):
        return f"({self.lx},{self.rx},{self.y})"
    def can_move(self,m,warehouse):
        # Horizontal cases are easier
        if m in ['<','>']:
            ny = self.y
            if m == '>':
                nx = self.rx + 1
            else:
                nx = self.lx -1
            if warehouse[ny][nx] == ".":
                return True
            elif warehouse[ny][nx] == "#":
                return False
            else:
                #Must be another crate
                next_crate = find_crate(nx,ny)
                return next_crate.can_move(m,warehouse)
        else:
            # Vertical moves - have to watch out for two spaces:
            ny = self.y - 1 if m == "^" else self.y + 1
            # these are the spaces we're trying to move into
            pt1 = warehouse[ny][self.lx]
            pt2 = warehouse[ny][self.rx]
            if pt1=="#" or pt2=="#":
                return False
            elif pt1=="." and pt2 == ".":
                return True
            else:
                # not a wall, at least one space is a crate                
                c1 = find_crate(self.lx,ny) if pt1 in self.crate_bits else None
                c2 = find_crate(self.rx,ny) if pt2 in self.crate_bits else None
                # check if all crates in our path can move
                cm1 = c1.can_move(m,warehouse) if c1 != None else True
                cm2 = c2.can_move(m,warehouse) if (c2 != None and c2!=c1) else True
                return cm1 and cm2
    def move(self,m,warehouse):   
        # Horizontal cases are easier
        if m in ['<','>']:
            nx = self.rx + 1 if m == '>' else self.lx -1
            if warehouse[self.y][nx] != ".":
                next_crate = find_crate(nx,self.y)
                next_crate.move(m,warehouse)
            if m == '>':
                swap((self.rx,self.y),(nx,self.y),warehouse)
                swap((self.lx,self.y),(self.rx,self.y),warehouse)
                self.lx = self.rx
                self.rx = nx
            else:
                swap((self.lx,self.y),(nx,self.y),warehouse)
                swap((self.lx,self.y),(self.rx,self.y),warehouse)
                self.rx = self.lx
                self.lx = nx
        else:
            # vertical moves
            nry = self.y - 1 if m == "^" else  self.y + 1
            # move any crates in our way
            pt1  = warehouse[nry][self.rx]
            pt2  = warehouse[nry][self.lx]
            c1 = find_crate(self.rx,nry) if pt1 in self.crate_bits else None
            c2 = find_crate(self.lx,nry) if pt2 in self.crate_bits else None
            if c1 != None:
                c1.move(m,warehouse)
            if c2 != None and c2 != c1:
                c2.move(m,warehouse)
            swap((self.lx,self.y),(self.lx,nry),warehouse)
            swap((self.rx,self.y),(self.rx,nry),warehouse)
            self.y = nry



def dprint(fs):
    if debug:
        print(fs)

def read_data_file(fname):
    df = open(fname, "r")
    fs = df.read()
    lines = fs.split('\n')
    warehouse = []
    moves = ""
    for l in lines:
        if l.startswith('#'):
            warehouse.append([r for r in l])
        else:
            moves += l
    return warehouse,[m for m in moves]

def read_and_convert_data_file(fname):
    print(f"Reading and converting: {fname}")
    df = open(fname, "r")
    fs = df.read()
    lines = fs.split('\n')
    warehouse = []
    moves = ""
    for l in lines:
        if l.startswith('#'):
            newline = []
            for r in l:
                if r == '#':
                    newline += ['#', '#']
                elif r == ".":
                    newline += ['.','.']
                elif r == "O":
                    newline += ['[',']']
                elif r == '@':
                    newline += ['@','.']
                else:
                    print(f"**** Unexpected character in input: {r}")
            warehouse.append(newline)
        else:
            moves += l
    return warehouse,[m for m in moves]

def find_robot(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == '@':
                return (x,y)
    return (-1,-1)

def find_all_crates(grid):
    crates = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == '[':
                crates.append(Crate(x,x+1,y))
    return crates

Directions = Enum('Directions', [ ('^', (0,-1)), ('>',(1,0)),('v',(0,1)), ('<',(-1,0))])

def draw_w_from_crates(warehouse):
    global crates
    # create new grid
    new_grid = []
    for l in warehouse:
        new_grid.append(['.' for i in range(len(l))])   
    for c in crates:
        new_grid[c.y][c.lx] = '['
        new_grid[c.y][c.rx] = ']'
    for line in new_grid:
        print(''.join([str (i) for i in line]))
    return new_grid

def next_pos(start,dir):
    global Directions
    (x,y) = start
    (dx,dy) = Directions[dir].value
    return (x+dx,y+dy)
  
def swap(a,b,warehouse):   
    (ax,ay) = a
    (bx,by) = b
    temp = warehouse[by][bx]
    if temp == "#":
        print(f"*** you seem to be moving a wall piece - swap({a},{b})")
    warehouse[by][bx] = warehouse[ay][ax]
    warehouse[ay][ax] = temp


def move_robot(m,robot_pos,warehouse):
    global crate_bits
    (nx,ny) = next_pos(robot_pos,m)    
    if warehouse[ny][nx] == ".":
        # easy case first
        swap( (robot_pos), (nx,ny), warehouse)
        robot_pos = (nx,ny)
    elif warehouse[ny][nx] in crate_bits:
        # There's a crate in the way
        c = find_crate(nx,ny)
        if c.can_move(m,warehouse):
            c.move(m,warehouse)
            swap( (robot_pos), (nx,ny), warehouse)
            robot_pos = (nx,ny)

    return robot_pos

def print_grid(grid):
    for line in grid:
        print(''.join([str (i) for i in line]))

def find_crate(x,y) -> Crate:
    global crates
    for c in crates:
        if( c.lx== x or c.rx==x ) and c.y==y:
            return c
    return None

if __name__ == '__main__':
    button_costs = [3,1]
    print(f"*** Day 15, Part 1 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True

    filename = sys.argv[1]
    if 'aoc' in filename:
        warehouse,moves = read_and_convert_data_file(sys.argv[1])
    else:
        warehouse,moves = read_data_file(sys.argv[1])
    dprint(f"Warehouse: {len(warehouse[0])} x {len(warehouse)})")
    robot_pos = find_robot(warehouse)
    dprint(f"Robot: {robot_pos}")
    crates = find_all_crates(warehouse)
    dprint(f"Crates: {len(crates)}")
    dprint(f"Moves: {len(moves)}")
    if debug:
        print_grid(warehouse)    
    for m in moves:
        dprint(f"Move: {m}, robot: {robot_pos}")
        robot_pos = move_robot(m,robot_pos,warehouse)
        if debug:
            print_grid(warehouse)
    print_grid(warehouse)

    gps_total = 0     
    height = len(warehouse)
    width = len(warehouse[0])
    dprint(f"Height: {height}, width: {width}")
    for c in crates:
        gps_total += (100*c.y + c.lx)


    print(f"Total of crate GPS values: {gps_total}")