import csv
import os
import subprocess
import os
import yaml
import pdb

def creat_output_csv(agent_num, scens):
    directory = "../Data/Results_best/AnimeDemo/dcpOEGAT/map32x32_rho1_{}Agent/K2_HS0/TR_M20p1_10Agent/1602191363/Project_G/exp_multinorm/commR_7".format(agent_num)

    # Create a CSV file
    csv_file_path = directory + '/output.csv'
    cases = range(1, scens+1)

    # Write the values to the CSV file
    with open(csv_file_path, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['magatCost', 'magatMakespan', 'magatSucceed', 'ECBSCost', 'ECBSMakespan'])

        for case in cases:
            with open(directory + '/predict/predict_map32x32_IDMap00000_IDCase{:05d}.yaml'.format(case), 'r') as file:
                predict = yaml.safe_load(file)

            with open(directory + '/target/expert_map32x32_IDMap00000_IDCase{:05d}.yaml'.format(case), 'r') as file:
                target = yaml.safe_load(file)

            magat_statistics = predict.get('statistics', {})
            magat_cost = magat_statistics.get('cost', None)
            magat_makespan = magat_statistics.get('makespan', None)
            succeed = magat_statistics.get('succeed', None)

            ECBS_statistics = target.get('statistics', {})
            ECBS_cost = ECBS_statistics.get('cost', None)
            ECBS_makespan = ECBS_statistics.get('makespan', None)

            csv_writer.writerow([magat_cost, magat_makespan, succeed, ECBS_cost, ECBS_makespan])

def visualize(agent, cases, seed):
    print("Starting visualization!")
    directory = "../Data/Results_best/AnimeDemo/dcpOEGAT/map32x32_rho1_{}Agent/K2_HS0/TR_M20p1_10Agent/1602191363/Project_G/exp_multinorm/commR_7/".format(agent)
    if not os.path.exists(directory + "gifs"):
        os.makedirs(directory + "gifs")
    for case in range(cases):
         subprocess.call(["python3", "../utils/visualize.py",
                             "--map", directory + "input/input_map32x32_IDMap00000_IDCase{:05d}.yaml".format(case+1),
                             "--schedule", directory + "predict/predict_map32x32_IDMap00000_IDCase{:05d}.yaml".format(case+1),
                             "--GSO", directory + "GSO/predict_map32x32_IDMap00000_IDCase{:05d}.mat".format(case+1),
                             "--speed", "2",
                             "--video", directory + "gifs/IDCase{:05d}_Seed{}.gif".format(case+1, seed),
                             "--nGraphFilterTaps", "2",
                             "--id_chosenAgent", "0"])
    print("Ending visualization!")

if __name__ == '__main__':

    agents = range(50, 450+1, 100)
    num_scens = 10
    seeds = range(1,6)

    for agent in agents:
        directory = "../Data/Results_best/AnimeDemo/dcpOEGAT/map32x32_rho1_{}Agent/K2_HS0/TR_M20p1_10Agent/1602191363/Project_G/exp_multinorm/commR_7".format(agent)

        # Create a CSV file
        csv_file_path = directory + '/output.csv'
        file_exists = os.path.exists(csv_file_path)
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            # csv_writer.writerow(['magatCost', 'magatMakespan', 'magatSucceed', 'ECBSCost', 'ECBSMakespan'])

        for seed in seeds:
            command = """python ../main.py ../configs/dcpGAT_OE_Random.json --mode test --best_epoch --test_general --log_time_trained 1602191363 \
    --test_checkpoint --nGraphFilterTaps 2 --trained_num_agents 10 --trained_map_w 20 --commR 7 --list_map_w 32 \
    --GSO_mode dist_GSO --action_select exp_multinorm --guidance Project_G \
    --CNN_mode ResNetLarge_withMLP --batch_numAgent --test_num_processes 0 --nAttentionHeads 1 --attentionMode KeyQuery \
    --tb_ExpName DotProduct_GAT_Resnet_3Block_distGSO_baseline_128 --log_anime --shieldType=LaCAM \
    --list_agents={} --list_num_testset={} --seed={} --pibt_r=0.001""".format(agent, num_scens, seed)
            tmp = [str(x) for x in command.split(" ") if x != ""]
            # pdb.set_trace()
            subprocess.run(tmp, check=True)
            creat_output_csv(agent, num_scens)
            # visualize(agent, num_scens, seed)

    # for agent in agents:
    #     creat_output_csv(agent)

"""
python ../main.py ../configs/dcpGAT_OE_Random.json --mode test --best_epoch --test_general --log_time_trained 1602191363 \
    --test_checkpoint --nGraphFilterTaps 2 --trained_num_agents 10 --trained_map_w 20 --commR 7 --list_map_w 32 \
    --list_num_testset 10 --GSO_mode dist_GSO --action_select exp_multinorm --guidance Project_G \
    --CNN_mode ResNetLarge_withMLP --batch_numAgent --test_num_processes 0 --nAttentionHeads 1 --attentionMode KeyQuery \
    --tb_ExpName DotProduct_GAT_Resnet_3Block_distGSO_baseline_128 --log_anime --shieldType=LaCAM --seed=1 --list_agents 100 \
    --pibt_r=0.001
"""
