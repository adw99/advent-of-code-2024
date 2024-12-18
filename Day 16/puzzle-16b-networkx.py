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

def build_graph(grid):
    G = nx.Graph()
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
            (xinc,yinc) = d.value
            newx = pt_x + xinc
            newy = pt_y + yinc
            if grid[newy][newx] == '.':
                G.add_edge( (pt_x,pt_y,d.name),(newx,newy,d.name),weight=1 )
            if d.name!= pt_dir:
                G.add_edge( pt, (pt_x,pt_y,d.name),weight=1000)

    # special case for end
    (x,y) = end
    G.add_node((x,y,'?'))
    for d in Directions:
        G.add_edge( (x,y,d.name),(x,y,'?'),weight=0)

    dprint(f"Nodes>{len(list(G.nodes))}")
    dprint(f"Edges>{len(list(G.edges))}")
    return G

def path_dist(G,target):
    return nx.single_source_dijkstra(G, source=target, weight='weight')

if __name__ == '__main__':
    button_costs = [3,1]
    print(f"*** Day 16, Part 2 ***\n")
    if(len(sys.argv) >=3 and sys.argv[2] == 'debug'):
        debug = True
    grid = read_data_file(sys.argv[1])
    start = find_char(grid,'S')
    end = find_char(grid,'E')
    dprint(f"Start:{start}, End: {end}")
    
    (x,y) = start
    G = build_graph(grid)
    print(f"Nodes: {len(G.nodes)}")
    print(f"Edges: {len(G.edges)}")

    start_pt = (x,y,Directions.RIGHT.name)
    (x,y) = end
    end_pt = (x,y,'?')
    dprint(f"Start point: {start_pt} / {Directions.RIGHT.name}")
    dprint(f"Grid built, solving....")
    score = nx.shortest_path_length(G, start_pt, end_pt, weight="weight")
    print(f"Shortest path? : {score}")
    
    # Find nodes that are on any of the shortest paths
    dprint("Finding Djikstra's.....")
    dist_from_start, _ = nx.single_source_dijkstra(G, source=start_pt, weight='weight')
    dist_from_end, _   = nx.single_source_dijkstra(G, source=end_pt, weight='weight')    
    
    # dist_from_start, _ = nx.single_source_bellman_ford(G, source=start_pt, weight='weight')
    # dist_from_end, _   = nx.single_source_bellman_ford(G, source=end_pt, weight='weight')    

    
    min_cost = dist_from_start[end_pt]
    mc2 = dist_from_end[start_pt]
    dprint(f"Min cost?: {min_cost} / {mc2}")
    dprint("Finding chairs....")
    chairs = []
    for pt in G.nodes():
        (x,y,d) = pt
        if( dist_from_start[pt] + dist_from_end[pt] == min_cost ):
            if not (x,y) in chairs:
                chairs.append((x,y))
    print(f"Chairs: {len(chairs)}")
    # dprint(f"Chair list: {chairs}")
