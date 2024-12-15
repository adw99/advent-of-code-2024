import sys
import re
import copy 
import math

debug = False

class Position:
    def __init__(self,x,y):
        self.x = int(x)
        self.y = int(y)
    def __str__(self):
        return f"({self.x},{self.y})"

class Velocity:
    def __init__(self,vx,vy):
        self.vx = int(vx)
        self.vy = int(vy)
    def __str__(self):
        return f"({self.vx},{self.vy})"
    
class Robot:
    def __init__(self,pos,vel):
        self.start = pos
        self.curr = copy.deepcopy(pos)
        self.vel = vel
    def __str__(self):
        return f"{self.start} => {self.curr} ({self.vel})"
    def move(self,moves,max_x,max_y):
        self.curr.x = (self.curr.x + moves*self.vel.vx) % max_x
        self.curr.y = (self.curr.y + moves*self.vel.vy) % max_y


def dprint(fs):
    if debug:
        print(fs)

def read_data_file(fname):

    line_rex = re.compile("p=(\\d+),(\\d+) v=(-?\\d+),(-?\\d+)")

    df = open(fname, "r")
    fs = df.read()
    lines = fs.split('\n')
    robots = []
    for l in lines:
        m = line_rex.search(l)
        pos = Position(m[1],m[2])
        vel = Velocity(m[3],m[4])
        rob = Robot(pos,vel)
        robots.append(rob)
    return robots

def draw_robots(robots,width,height):
    grid = []
    # populate grid with periods
    for lines in range(height):
        grid.append(['.']*width)
    # add robot counts
    for r in robots:
        grid[r.curr.y][r.curr.x] = '*'
    return grid

def print_grid(grid):
    for line in grid:
        dprint(''.join([str (i) for i in line]))


def find_long_row(grid):
    longest = 0
    for line in grid:
        prev = '.'
        curr_count = 0
        for x in range(len(line)):
            curr = line[x]
            if curr == '.':
                # did we just end a segment ?
                if prev == '*':
                    # yes, check if longest
                    if curr_count > longest:
                        longest = curr_count
                curr_count = 0
            else: 
                # we are in a segment, even if it's the first star
                curr_count += 1
            prev = curr
    return longest

if __name__ == '__main__':
    button_costs = [3,1]
    print(f"*** Day 14, Part 2 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True

    robots = read_data_file(sys.argv[1])
    dprint(f"Machine count: {len(robots)}")
    if len(robots) == 12:
        # sample data
        width = 11
        height = 7
    else:
        # actual input 
        width = 101
        height = 103
    time = 10000 

    longest_row = 0
    longest_row_time = 0
    for t in range(time):
        for r in robots:
            r.move(1,width,height)
        grid = draw_robots(robots,width,height)
        long = find_long_row(grid)        
        if long > longest_row:
            longest_row = long
            longest_row_time = t
            if long > 10:
                print_grid(grid)
                dprint(f"Time: {t+1}")

    print(f"Time of longest row: {longest_row_time+1}, longest row: {longest_row}")
