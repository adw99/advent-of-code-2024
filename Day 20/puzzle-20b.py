import sys
from enum import Enum
import copy
import heapq
import math
from collections import defaultdict

debug = False

def dprint(fs):
    if debug:
        print(fs)

def read_data_file(fname):
    grid = []
    df = open(fname, "r")
    lines = df.read().splitlines()
    for l in lines:
        grid.append([r for r in l])

    return grid

def print_grid(grid):
    for line in grid:
        print(''.join([str (i) for i in line]))

def print_trail(trail,master_grid):
    grid = copy.deepcopy(master_grid)
    for pt in trail:
        (x,y) = pt
        char = grid[y][x]
        if char == ".":
            char = "*"
        grid[y][x] = f"{bcolors.OKCYAN}{char}{bcolors.ENDC}"
    print_grid(grid)

def find_char(grid,target):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == target:
                return (x,y)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

Directions = Enum('Directions', [ ('UP', (0,-1)), ('RIGHT',(1,0)),('DOWN',(0,1)), ('LEFT',(-1,0))])

class DPoint:
    def __init__(self,x,y,shortest_distance,prev_node,dir):
        self.x = x
        self.y = y
        self.shortest_distance = shortest_distance
        self.prev_node = prev_node
    def __str__(self):
        return f"({self.x},{self.y}): {self.shortest_distance}/{self.prev_node}/{self.dir}"
    def __lt__(self, other):
        return self.shortest_distance < other.shortest_distance

def build_dijkstra(start,grid):
    distances = []
    unvisited_nodes = []
    distances = [[None for cols in range(len(grid[0]))] for rows in range(len(grid))]

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] in (".","S","E"):
                distances[y][x]=DPoint(x,y,float('inf'),None,None)
                unvisited_nodes.append((x,y,))

    (x,y) = start
    pt = distances[y][x]
    pt.shortest_distance = 0
    unvisited_nodes.remove((x,y))
    q = []
    heapq.heappush( q,pt )

    while q:
        pt = heapq.heappop(q)
        # dprint(f"\n({pt.x},{pt.y}): {pt.dir} \n")
        for d in Directions:
            (xinc,yinc) = d.value
            newx = pt.x + xinc
            newy = pt.y + yinc
            if 0 <= newy < len(grid) and 0 <= newx < len(grid[0]) and grid[newy][newx] !='#':
                newpt = distances[newy][newx]
                if( (newx,newy) in unvisited_nodes):
                    unvisited_nodes.remove((newx,newy))
                new_dist = pt.shortest_distance + 1
                if new_dist < newpt.shortest_distance:
                    newpt.shortest_distance = new_dist
                    newpt.prev_node = (pt.x,pt.y)
                    newpt.dir = d
                    heapq.heappush(q,newpt)

    return distances

def skipable(x,y,grid):
    rows = len(grid)
    cols = len(grid[0])
    return grid[y][x] == "#" and not x in [0,cols-1] and not y in [0,rows-1]

def build_trail(end,start,distances):
    trail = []
    pt = end
    while pt != None:
        trail.append(pt)
        (x,y) = pt
        pt = distances[y][x].prev_node

    return trail

def manhattan(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

if __name__ == '__main__':
    button_costs = [3,1]
    print(f"*** Day 20, Part 2 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    fname = sys.argv[1] if len(sys.argv) >=2 else 'sample.txt' 
    grid = read_data_file(fname)
    # print_grid(grid)
    start = find_char(grid,'S')
    end = find_char(grid,'E')
    distances = build_dijkstra(start,grid)
    (endx,endy) = end
    orig_score = distances[endy][endx].shortest_distance
    print(f"Initial score: {orig_score}")
    trail = build_trail(end,start,distances)
    if debug:
        print_trail(trail,grid)

    rev_distances = build_dijkstra(end,grid)

    max_cheat = 20    
    thresh_count = 0
    (startx,starty) = start
    rows = len(grid)
    cols = len(grid[0])
    thresh = 50 if rows==15 else 100
    cheat_thresh_count = 0

    cheat_set = defaultdict(int)
    radius = max_cheat
    (endx,endy) = end

    # for every point in the trail, compare to every other point in the trail
    # see if there is a cheat between the two that saves {thresh} ps
    for pt1 in reversed(trail):
        (x1,y1) = pt1
        dist1 = rev_distances[y1][x1].shortest_distance
        for pt2 in trail:
            (x2,y2) = pt2
            dist2 = rev_distances[y2][x2].shortest_distance
            d = manhattan(pt1,pt2)
            if d<=max_cheat:
                cheat = dist1-dist2-d
                dprint(f"{x1},{y1},{x2},{y2} => {dist1},{dist2},{d} = {cheat}")
                if cheat >= thresh:
                    cheat_thresh_count += 1
                    cheat_set[cheat] += 1



    for k in cheat_set.keys():
        dprint(f"{cheat_set[k]} shortcuts saved {k} ps")
    print(f"Cheats that saved over {thresh} ps: {cheat_thresh_count}")