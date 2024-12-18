import sys
from enum import Enum
import copy
import networkx as nx
import matplotlib.pyplot as plt

debug = False

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

Directions = Enum('Directions', [ ('UP', (0,-1)), ('RIGHT',(1,0)),('DOWN',(0,1)), ('LEFT',(-1,0))])
Opp_Dir = Enum('OPPOSITE Direction', [ ('UP', 'DOWN'), ('RIGHT','LEFT'), ('DOWN','UP'), ('LEFT', 'RIGHT')])

def build_graph(grid,G):
    nodes = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] in ['.','S','E']:
                for d in Directions:
                    nodes.append((x,y,d.name))
                    G.add_node((x,y,d.name))
    for pt in nodes:
        # add edges that represent turns
        (pt_x,pt_y,pt_dir) = pt
        for d in Directions:
            if d.name!= pt_dir:
                G.add_edge( pt, (pt_x,pt_y,d.name),weight=1000)
                if d != Opp_Dir[pt_dir]:
                    (xinc,yinc) = d.value
                    newx = pt_x + xinc
                    newy = pt_y + yinc
                    if grid[newy][newx] == '.':
                        G.add_edge( (pt_x,pt_y,d.name),(newx,newy,d.name),weight=1 )

    # special case for end
    (x,y) = end
    end_spec = (x,y,'?')
    G.add_node(end_spec)
    for d in Directions:
        G.add_edge( (x,y,d.name),end_spec,weight=0)

    dprint(f"Nodes>{len(list(G.nodes))}")
    dprint(f"Edges>{len(list(G.edges))}")


def build_edges(grid,G,start,end):
    q = [start]
    count = 0
    visited = [start]
    while len(q)>0:
        pt = q.pop()
        (x,y,pt_dir) = pt
        visited.append((x,y))
        for d in Directions:            
            (xinc,yinc) = d.value
            newx = x + xinc
            newy = y + yinc
            if grid[newy][newx] in [".","E"]:

                eweight = 1 if d == pt_dir else 1001
                G.add_edge((x,y),(newx,newy),weight=eweight)
                count +=1
                if (newx,newy) not in visited:
                    q.append((newx,newy,d))
    dprint(f"Edges added to graph: {count}")



if __name__ == '__main__':
    button_costs = [3,1]
    print(f"*** Day 16, Part 2 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    grid = read_data_file(sys.argv[1])
    G = nx.Graph()
    start = find_char(grid,'S')
    end = find_char(grid,'E')
    dprint(f"Start:{start}, End: {end}")
    (x,y) = start
    build_graph(grid,G)
    start_pt = (x,y,Directions.RIGHT.name)
    (x,y) = end
    end_pt = (x,y,'?')
    dprint(f"Start point: {start_pt} / {Directions.RIGHT.name}")
    dprint(f"Grid built, solving....")
    score = nx.shortest_path_length(G, start_pt, end_pt, weight="weight")
    print(f"Shortest path? : {score}")
    # all_paths = nx.all_shortest_paths(G, start_pt, end_pt, weight="weight")  #, method = 'bellman-ford'
    # chairs = set([(x[0], x[1]) for pt in all_paths for x in pt])    
    # chair_count = len(chairs)
    # print(f"Number of chairs: {chair_count}")