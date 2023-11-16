import subprocess

agents = range(10, 110+1, 30)

for agent in agents:
    subprocess.call(["python", "../main.py",
                     "../configs/dcpGAT_OE_Random.json",
                     "--mode", "test",
                     "--best_epoch",
                     "--test_general",
                     "--log_time_trained", "1602191363",
                     "--test_checkpoint",
                     "--nGraphFilterTaps", "2",
                     "--trained_num_agents", "10",
                     "--trained_map_w", "20",
                     "--commR", "7",
                     "--list_map_w", "32",
                     "--list_agents", str(agent),
                     "--list_num_testset", "10",
                     "--GSO_mode", "dist_GSO",
                     "--action_select", "exp_multinorm",
                     "--guidance", "Project_G",
                     "--CNN_mode", "ResNetLarge_withMLP",
                     "--batch_numAgent",
                     "--test_num_processes", "0",
                     "--nAttentionHeads", "1",
                     "--attentionMode", "KeyQuery",
                     "--tb_ExpName", "DotProduct_GAT_Resnet_3Block_distGSO_baseline_128",
                     "--log_anime",
                     "--shieldType=LaCAM"
                     ])

"""
python ../main.py ../configs/dcpGAT_OE_Random.json --mode test --best_epoch --test_general --log_time_trained 1602191363 \
    --test_checkpoint --nGraphFilterTaps 2 --trained_num_agents 10 --trained_map_w 20 --commR 7 --list_map_w 32 \
    --list_agents 100 --list_num_testset 10 --GSO_mode dist_GSO --action_select exp_multinorm --guidance Project_G \
    --CNN_mode ResNetLarge_withMLP --batch_numAgent --test_num_processes 0 --nAttentionHeads 1 --attentionMode KeyQuery \
    --tb_ExpName DotProduct_GAT_Resnet_3Block_distGSO_baseline_128 --log_anime
"""