import sys
from enum import Enum
import copy
import heapq

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
    for ln in range(time):
        nums = lines[ln].split(',')
        grid[int(nums[0])][int(nums[1])] = "#"
        drops.append((int(nums[0]),int(nums[1])))
    return grid,drops,dim

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
    dprint("Running Djikstra")
    q = []
    heapq.heappush( q,pt )

    while q:
        pt = heapq.heappop(q)
        # dprint(f"\n({pt.x},{pt.y}): {pt.dir} \n")
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

if __name__ == '__main__':
    button_costs = [3,1]
    print(f"*** Day 16, Part 2 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    grid,drops,dim = read_data_file(sys.argv[1])
    print_grid(grid)
    distances = build_dijkstra((0,0), grid)
    end = distances[dim-1][dim-1]
    print(f"Score: {end.shortest_distance}")

