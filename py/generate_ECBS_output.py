import os
import subprocess

import yaml

agents = range(50, 450+1, 50)
scens = range(1, 25+1)

for agent in agents:
    for scen in scens:
        output_path = "../maps/map32x32_density_p1/{}_Agent/output_ECBS/output_map32x32_IDMap00000_IDCase{:05d}.yaml".format(agent, scen)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        # with open("../maps/map32x32_density_p1/{}_Agent/input/input_map32x32_IDMap00000_IDCase{:05d}.yaml".format(agent, scen), 'r') as file:
        #     data = yaml.safe_load(file)
        #
        # f = open(output_path, 'w')
        # f.write("statistics:\n")
        # f.write("  cost: {}\n".format(9999))
        # f.write("  makespan: {}\n".format(100))
        # f.write("  runtime: {}\n".format(1))
        # f.write("  highLevelExpanded: {}\n".format(100))
        # f.write("  lowLevelExpanded: {}\n".format(100))
        # f.write("schedule:\n")
        # for a in range(agent):
        #     f.write("  agent{}:\n".format(a))
        #     f.write("    - x: {}\n".format(data['agents'][a]['start'][0]))
        #     f.write("      y: {}\n".format(data['agents'][a]['start'][1]))
        #     f.write("      t: {}\n".format(0))
        #     f.write("    - x: {}\n".format(data['agents'][a]['goal'][0]))
        #     f.write("      y: {}\n".format(data['agents'][a]['goal'][1]))
        #     f.write("      t: {}\n".format(1))
        # f.close()

        subprocess.call(["../offlineExpert/ecbs",
                         "-i", "../maps/map32x32_density_p1/{}_Agent/input/input_map32x32_IDMap00000_IDCase{:05d}.yaml".format(agent, scen),
                         "-o", output_path,
                         "-w", str(2)],
                         cwd="../offlineExpert")
