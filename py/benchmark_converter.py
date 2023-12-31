
"""
This script is designed to take standard MAPF benchmark problems
(https://movingai.com/benchmarks/mapf/index.html) and convert them into YAML
files used by the example implementations provided by libMultiRobotPlanning.
"""
import os
import argparse

# Ex: python benchmark_converter.py ../maps/benchmark/random-32-32-10/scen-random/random-32-32-10-random-{}.scen ../maps/benchmark/random-32-32-10/random-32-32-10.map
def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("scenario", type=str, help=".scen Scenario file")
    parser.add_argument("map", type=str, help=".map Map file")
    # parser.add_argument("output_prefix", type=str, help=".yaml Output file prefix")
    return parser.parse_args()


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


def load_map_file(map_file, occupied_char={'@', 'T', 'O'}, valid_chars={'@', '.', 'T', 'G', 'O', 'S', 'W'}):
    if not os.path.isfile(map_file):
        print("Map file not found!")
        exit(-1)
    map_ls = open(map_file, 'r').readlines()
    height = int(map_ls[1].replace("height ", ""))
    width = int(map_ls[2].replace("width ", ""))
    map_ls = map_ls[4:]
    map_ls = [l.replace('\n', '') for l in map_ls]
    occupancy_lst = set()
    assert(len(map_ls) == height)
    for y, l in enumerate(map_ls):
        assert(len(l) == width)
        for x, c in enumerate(l):
            assert(c in valid_chars)
            if c in occupied_char:
                occupancy_lst.add((x, y))
    return width, height, occupancy_lst


def load_scenario_file(scen_file,
                       occupancy_list,
                       map_width,
                       map_height):
    if not os.path.isfile(scen_file):
        print("Scenario file not found!")
        exit(-1)
    ls = open(scen_file, 'r').readlines()
    if "version 1" not in ls[0]:
        print(".scen version type does not match!")
        exit(-1)
    instances = [convert_nums(l.split('\t')) for l in ls[1:]]
    # instances.sort(key=lambda e: e[0])
    for i in instances:
        assert(i[2] == map_width)
        assert(i[3] == map_height)
    # ((sx, sy), (gx, gy))
    instances = [((i[4], i[5]), (i[6], i[7])) for i in instances]
    for start, goal in instances:
        assert(start not in occupancy_list)
        assert(goal not in occupancy_list)
    return instances


def generate_sliced_problems(instances,
                             scen,
                             map_width,
                             map_height,
                             occupancy_list,
                             file_pattern,
                             min_agents=10,
                             agent_step=10):
    for agent_count in range(min_agents, len(instances) + 1, agent_step):
        file_name = file_pattern.format(agent_count, scen)
        print("Generating", file_name)
        dump_yaml(instances[:agent_count],
                  map_width,
                  map_height,
                  occupancy_list,
                  file_name)


def dump_yaml(instances, map_width, map_height, occupancy_list, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    f = open(filename, 'w')
    f.write("map:\n")
    f.write("    dimensions: {}\n".format([map_width, map_height]))
    f.write("    obstacles:\n")
    for o in occupancy_list:
        f.write("    - {}\n".format(list(o)))
    f.write("agents:\n")
    for idx, i in enumerate(instances):
        f.write("""-   goal: {}
    name: agent{}
    start: {}
""".format(list(i[1]), idx, list(i[0])))
    f.close()


args = setup_args()
print("Loading map")
map_width, map_height, occupancy_list = load_map_file(args.map)
print("Map loaded")
print("Loading scenario file")
for scen_num in range(1, 26):

    instances = load_scenario_file(args.scenario.format(scen_num),
                                   occupancy_list,
                                   map_width,
                                   map_height)
    print("Scenario loaded")
    generate_sliced_problems(instances,
                             scen_num,
                             map_width,
                             map_height,
                             occupancy_list,
                             "../maps/map32x32_density_p1/{}_Agent/input/input_map32x32_IDMap00000_IDCase{:05d}.yaml")
