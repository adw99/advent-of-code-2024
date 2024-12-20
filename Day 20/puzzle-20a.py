import sys
from enum import Enum
import copy
import heapq
import math

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
        grid[y][x] = f"{bcolors.OKCYAN}*{bcolors.ENDC}"
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



def find_largest_gain(x,y,grid,distances):
    # find the largest delta across this point, vertically or horizontally
    gain = 0
    rows = len(grid)
    cols = len(grid[0])
    leftx = x-1
    rightx = x+1
    if leftx >=0 and rightx < cols and grid[y][leftx] != '#' and grid[y][rightx] != '#':
        hgain = abs( distances[y][leftx].shortest_distance - distances[y][rightx].shortest_distance) - 2
        if hgain == math.inf:
            hgain = 0
    else:
        hgain = 0
    topy = y-1
    boty = y+1
    if topy >=0 and boty < rows and grid[topy][x] != '#' and grid[boty][x] != '#':
        vgain = abs( distances[topy][x].shortest_distance - distances[boty][x].shortest_distance) - 2
        if vgain == math.inf:
            vgain = 0
    else:
        vgain = 0
    return max(hgain,vgain)

def skipable(x,y,grid):
    rows = len(grid)
    cols = len(grid[0])
    targets = ('.','E')
    if grid[y][x] == "#" and not x in [0,cols-1] and not y in [0,rows-1]:
        return True
    else:
        return False            

def set_add(myset,val):
    if not val in myset:
        myset[val] = 1
    else:
        myset[val] = myset[val] + 1

if __name__ == '__main__':
    button_costs = [3,1]
    print(f"*** Day 20, Part 2 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    grid = read_data_file(sys.argv[1])
    print_grid(grid)
    start = find_char(grid,'S')
    end = find_char(grid,'E')
    distances = build_dijkstra(start,grid)
    (endx,endy) = end
    score = distances[endy][endx].shortest_distance
    print(f"Initial score: {score}")
    min_score = score
    save_thresh = 0
    best_gain = 0
    rows = len(grid)
    cols = len(grid[0])
    thresh = 20 if cols==15 else 100
    gain_set = {}
    count = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if skipable(x,y,grid):
                # only really care if there is 100+ difference to be gained
                pt_gain = find_largest_gain(x,y,grid,distances)
                if pt_gain>0:
                    count += 1
                set_add(gain_set,pt_gain)
                if pt_gain >=thresh:
                    # dprint(f"({x},{y}) shortcut saves: {pt_gain}")
                    save_thresh += 1
                if pt_gain > best_gain:
                    best_gain = pt_gain
    print(f"Routest that saved {thresh}+ ps: {save_thresh}")
    dprint(f"Largest gain: {best_gain}")
    # for k in gain_set.keys():
    #     dprint(f"{gain_set[k]} shortcuts saved {k} ps")