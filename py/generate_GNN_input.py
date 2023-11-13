import subprocess

agents = range(100, 110+1, 10)

for agent in agents:
    subprocess.call(["python", "../offlineExpert/DataGen_Transformer_split_IDMap.py",
                     "--num_agents", str(agent),
                     "--map_w", "32",
                     "--map_density", "0.1",
                     "--div_train", "0",
                     "--div_valid", "0",
                     "--div_test", "25",
                     "--div_train_IDMap", "0",
                     "--div_valid_IDMap", "0",
                     "--div_test_IDMap", "0",
                     "--solCases_dir",
                     "../maps",
                     "--dir_SaveData",
                     "../Data/DataSource_DMap_FixedComR/EffectiveDensity/Training",
                     "--guidance",
                     "Project_G"
                     ])
