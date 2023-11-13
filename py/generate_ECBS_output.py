import os
import subprocess

agents = range(10, 110+1, 10)
scens = range(1, 25+1)

for agent in agents:
    for scen in scens:
        output_path = "../maps/map32x32_density_p2/{}_Agent/output_ECBS/output_map32x32_IDMap00000_IDCase{:05d}.yaml".format(agent, scen)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        subprocess.call(["../offlineExpert/ecbs",
                         "-i", "../maps/map32x32_density_p2/{}_Agent/input/input_map32x32_IDMap00000_IDCase{:05d}.yaml".format(agent, scen),
                         "-o", output_path,
                         "-w", str(1.1)],
                         cwd="../offlineExpert")
