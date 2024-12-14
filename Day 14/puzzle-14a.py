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
        dprint(rob)
        robots.append(rob)
    return robots

def draw_robots(robots,width,height):
    grid = []
    # populate grid with periods
    for lines in range(height):
        grid.append(['.']*width)
    # add robot counts
    for r in robots:
        if grid[r.curr.y][r.curr.x] == '.':
            grid[r.curr.y][r.curr.x] = 1
        else:
            grid[r.curr.y][r.curr.x] += 1 
    return grid

def print_grid(grid):
    for line in grid:
        dprint(''.join([str (i) for i in line]))

def count_quad(grid,xmin,xmax,ymin,ymax):
    count = 0
    # dprint(f"Quad: y:{ymin} + {list(range(ymax-ymin))}, x:{xmin} + {list(range(xmax-xmin))}")
    for y in range(ymax-ymin):
        for x in range(xmax-xmin):
            pt = grid[ymin+y][xmin+x]

            if pt!= '.':
                count += pt
    return count

def count_quadrants(grid):
    height = len(grid)
    width = len(grid[0])
    midx = math.ceil(width/2) 
    midy = math.ceil(height/2)
    q1 = count_quad(grid,0,midx-1,0,midy-1)
    q2 = count_quad(grid,midx,width,0,midy-1)
    q3 = count_quad(grid,0,midx-1,midy,height)
    q4 = count_quad(grid,midx,width,midy,height)
    dprint(f"Quad counts: {q1}, {q2}, {q3}, {q4}")

    return q1 * q2 * q3 * q4


if __name__ == '__main__':
    button_costs = [3,1]
    print(f"*** Day 13, Part 1 ***\n")
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
    time = 100

    for r in robots:
        r.move(time,width,height)

    grid = draw_robots(robots,width,height)        
    print_grid(grid)

    safety_num = count_quadrants(grid)
    print(f"Safety factor: {safety_num}")
