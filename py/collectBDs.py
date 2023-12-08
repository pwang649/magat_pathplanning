import argparse
import heapq
import os

import numpy as np

def load_map_file(map_file):
    if not os.path.isfile(map_file):
        print("Map file not found!")
        exit(-1)
    map_ls = open(map_file, 'r').readlines()
    height = int(map_ls[1].replace("height ", ""))
    width = int(map_ls[2].replace("width ", ""))
    map_ls = map_ls[4:]
    map_ls = [l.replace('\n', '') for l in map_ls]
    return [[0 if cell == '.' else 1 for cell in line] for line in map_ls]

def convert_nums(l):
    for i in range(len(l)):
        try:
            l[i] = int(l[i])
        except ValueError:
            try:
                l[i] = float(l[i])
            except ValueError:
                ""
    return l

def load_scenario_file(scen_file, grid_map):
    if not os.path.isfile(scen_file):
        print("Scenario file not found!")
        exit(-1)
    ls = open(scen_file, 'r').readlines()
    if "version 1" not in ls[0]:
        print(".scen version type does not match!")
        exit(-1)
    instances = [convert_nums(l.split('\t')) for l in ls[1:]]
    # instances.sort(key=lambda e: e[0])
    # ((sx, sy), (gx, gy))
    instances = [((i[4], i[5]), (i[6], i[7])) for i in instances]
    for start, goal in instances:
        assert(not np.isinf(grid_map[int(start[0])][int(start[0])]))
        assert(not np.isinf(grid_map[int(goal[0])][int(goal[0])]))
    return instances

def dijkstra_backward(grid, goal):
    rows, cols = len(grid), len(grid[0])
    distance = [[float('inf')] * cols for _ in range(rows)]

    # Priority queue to store (distance, node) tuples
    pq = [(0, goal)]
    distance[goal[0]][goal[1]] = 0

    while pq:
        dist, current = heapq.heappop(pq)

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_r, new_c = current[0] + dr, current[1] + dc

            if 0 <= new_r < rows and 0 <= new_c < cols:
                new_dist = dist + 1

                if new_dist < distance[new_r][new_c] and grid[new_r][new_c] == 0:
                    distance[new_r][new_c] = new_dist
                    heapq.heappush(pq, (new_dist, (new_r, new_c)))

    return distance

def generate_backward_dijkstra_info(grid, agents):
    backward_dijkstra_info = []

    for start, goal in agents:
        distance = dijkstra_backward(grid, goal)
        backward_dijkstra_info.append(distance)

    return backward_dijkstra_info

def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("scenario", type=str, help=".scen Scenario file")
    parser.add_argument("map", type=str, help=".map Map file")
    # parser.add_argument("output_prefix", type=str, help=".yaml Output file prefix")
    return parser.parse_args()

args = setup_args()
print("Loading map")
grid_map = load_map_file(args.map)
print("Map loaded")
print("Loading scenario file")

for scen_num in range(1, 26):
    agents_data = load_scenario_file(args.scenario.format(scen_num), grid_map)

    backward_dijkstra_info = generate_backward_dijkstra_info(grid_map, agents_data)

    backward_dijkstra_info = np.transpose(np.array(backward_dijkstra_info), (0, 2, 1))

    # Save NumPy array to a file
    np.save('BDs/random-32-32-10-scen-{}.npy'.format(scen_num), backward_dijkstra_info)
