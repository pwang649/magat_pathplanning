import csv

import yaml

agent_num = 10
directory = "../Data/Results_best/AnimeDemo/dcpOEGAT/map32x32_rho1_{}Agent/K2_HS0/TR_M20p1_10Agent/1602191363/Project_G/exp_multinorm/commR_7".format(agent_num)

# Create a CSV file
csv_file_path = directory + '/output.csv'
cases = range(1, 11)

# Write the values to the CSV file
with open(csv_file_path, 'w', newline='') as csv_file:
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

