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
    df = open(fname, "r")
    lines = df.read().splitlines()
    if 'sample' in fname:
        dim = 7
        time=12
    else:
        dim = 71
        time=1024
    grid = [['.' for cols in range(dim)] for rows in range(dim)]
    drops = []
    for ln in range(len(lines)):
        nums = lines[ln].split(',')
        x = int(nums[0])
        y = int(nums[1])
        drops.append((x,y))
        if ln < time:
            grid[y][x] = "#"
    return grid,drops,dim,time

def print_grid(grid):
    for line in grid:
        print(''.join([str (i) for i in line]))

def print_trail(trail,master_grid):
    grid = copy.deepcopy(master_grid)
    for pt in trail:
        (x,y) = pt
        grid[y][x] = f"{bcolors.OKCYAN}*{bcolors.ENDC}"
    print_grid(grid)

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
            if grid[y][x] == ".":
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
        for d in Directions:
            (xinc,yinc) = d.value
            newx = pt.x + xinc
            newy = pt.y + yinc
            if 0 <= newy < len(grid) and 0 <= newx < len(grid[0]) and grid[newy][newx] == '.':
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

def print_distances(grid,distances):
    for y in range(len(grid)):
        line = ''
        for x in range(len(grid[0])):
            if grid[y][x] == "#":
                line += "#####"
            else:
                line += '(' + str(distances[y][x].shortest_distance).zfill(3) + ')'
        print(line)

def find_path(grid,distances,end):
    path = []
    (x,y) = end
    score = distances[y][x].shortest_distance
    if score == math.inf:
        return []
    rows = len(grid)
    cols = len(grid[0])

    visited = []
    while score>0:
        for d in Directions:
            (xinc,yinc) = d.value
            newx = x+xinc
            newy = y+yinc
            if 0 <= newx < cols and 0 <= newy < rows and grid[newy][newx] == '.' and (newx,newy) not in visited:
                visited.append((newx,newy))
                if distances[newy][newx].shortest_distance == score-1:
                    path.append((newx,newy))
                    score = score - 1
                    x = newx
                    y = newy
                    break
    return path

if __name__ == '__main__':
    button_costs = [3,1]
    print(f"*** Day 18, Part 2 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    grid,drops,dim,time = read_data_file(sys.argv[1])
    print_grid(grid)
    
    distances = build_dijkstra((0,0), grid)
    end = distances[dim-1][dim-1]
    print(f"Initial score: {end.shortest_distance}")
    if debug:
        print_distances(grid,distances)
    path = find_path(grid,distances,(dim-1,dim-1))
    dprint(f"Path length: {len(path)}")
    for tick in range(time,len(drops)):
        (x,y) = drops[tick]
        grid[y][x] = '#'
        if (x,y) in path:            
            distances = build_dijkstra((0,0), grid)
            end = distances[dim-1][dim-1]
            print(f"{tick}) ({x},{y}): {end.shortest_distance}")
            if end.shortest_distance == math.inf:
                break
            else:
                path = find_path(grid,distances,(dim-1,dim-1))
        else:
                dprint(f"{tick}) ({x},{y}): not on shortest path")


