import sys
from enum import Enum
import copy
import heapq

debug = False
Directions = Enum('Directions', [ ('UP', (0,-1)), ('RIGHT',(1,0)),('DOWN',(0,1)), ('LEFT',(-1,0))])
Opp_Dir = Enum('OPPOSITE Direction', [ ('UP', 'DOWN'), ('RIGHT','LEFT'), ('DOWN','UP'), ('LEFT', 'RIGHT')])

def dprint(fs):
    if debug:
        print(fs)

def read_data_file(fname):
    df = open(fname, "r")
    fs = df.read()
    lines = fs.split('\n')
    warehouse = []
    for l in lines:
        warehouse.append([r for r in l])
    return warehouse

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

class DPoint:
    def __init__(self,x,y,shortest_distance,prev_node,dir):
        self.x = x
        self.y = y
        self.shortest_distance = shortest_distance
        self.prev_node = prev_node
        self.dir = dir
    def __str__(self):
        return f"({self.x},{self.y}): {self.shortest_distance}/{self.prev_node}/{self.dir}"
    def __lt__(self, other):
        return self.shortest_distance < other.shortest_distance

def build_dijkstra(start,distances,unvisited_nodes):
    (x,y) = start
    pt = distances[y][x]
    pt.shortest_distance = 0
    pt.dir = Directions.RIGHT
    unvisited_nodes.remove((x,y))
    dprint("Running Djikstra")
    q = []
    heapq.heappush( q,pt )

    while q:
        pt = heapq.heappop(q)
        # dprint(f"\n({pt.x},{pt.y}): {pt.dir} \n")
        dir = pt.dir
        for d in Directions:
            (xinc,yinc) = d.value
            newx = pt.x + xinc
            newy = pt.y + yinc
            if grid[newy][newx] in [".","E"] and d.name != Opp_Dir[dir.name].value:
                newpt = distances[newy][newx]
                if( (newx,newy) in unvisited_nodes):
                    unvisited_nodes.remove((newx,newy))
                delta = 1 if d == dir else 1001
                new_dist = pt.shortest_distance + delta
                if new_dist < newpt.shortest_distance:
                    newpt.shortest_distance = new_dist
                    newpt.prev_node = (pt.x,pt.y)
                    newpt.dir = d
                    if grid[newy][newx] == ".":
                        heapq.heappush(q,newpt)
                        # dprint(f"({x},{y}) => ({newx},{newy}): {d}/{dir} ({delta})")

def build_trail(end,distances):
    trail = []
    (x,y) = end
    pt = distances[y][x]
    while( pt != start and pt!= None):
        n = pt.prev_node
        if n != None:
            (x,y) = n
            pt = distances[y][x]
            dprint(f"> {pt}")
            trail.append((x,y))
        else:
            pt = None
    return trail

if __name__ == '__main__':
    button_costs = [3,1]
    print(f"*** Day 16, Part 1 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    grid = read_data_file(sys.argv[1])
    start = find_char(grid,"S")
    end = find_char(grid,"E")
    if debug:
        print_grid(grid)
        print(f"Start: {start}")
    distances = []
    for l in grid:
        distances.append([])
    unvisited_nodes = []
    visited_nodes = []
    dprint(f"Creating value list")
    for y in range(len(grid)):
        distances[y] = [None]*len(grid[y])
        for x in range(len(grid[y])):
            if grid[y][x] in [".","S","E"]:
                distances[y][x]=DPoint(x,y,float('inf'),None,None)
                unvisited_nodes.append((x,y,))
    build_dijkstra(start,distances,unvisited_nodes)
    dprint(f"Djikstra built?, remaining nodes: {len(unvisited_nodes)}:{unvisited_nodes}")
    (x,y) = end
    end_pt = distances[y][x]
    if debug:
        print_trail(build_trail(end,distances),grid)
    print(f"End node: {end_pt}")




            
            

