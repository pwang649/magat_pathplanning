import numpy as np
import matplotlib.pyplot as plt

# Arguments
rows = 3
cols = 4
num_agents = range(50, 150+1, 50)
scen = 1

def normalize(data):
    data = data / data.sum(axis=1, keepdims=True)
    return np.round(data, decimals=2)

def error_analysis(data):
    expected_matrix = np.array([[0.2, 0.2, 0.2, 0.2, 0.2],
                                [0.2, 0.2, 0.2, 0.2, 0.2],
                                [0.2, 0.2, 0.2, 0.2, 0.2],
                                [0.2, 0.2, 0.2, 0.2, 0.2],
                                [0.2, 0.2, 0.2, 0.2, 0.2]])

    # Calculate Mean Squared Error (MSE)
    mse = ((data - expected_matrix) ** 2).mean()
    return mse

def create_segmented_subplots(data, segment, agent):
    fig, axs = plt.subplots(rows, cols)

    for i, ax in enumerate(axs.flatten()):
        if i < len(data):
            img = ax.imshow(data[i])
        else:
            ax.remove()
    stopping_timestep = starting_timestep + rows * cols - 1
    plt.suptitle(f'num_agents: {agent}, scen: {scen}, timestep: {starting_timestep} to {stopping_timestep}')
    cbar = fig.colorbar(img, ax=axs, fraction=0.02, pad=0.04)
    plt.savefig('action_distribution_visualizations' + path_postfix + goal_postfix + '/num_agents_{}_scen_{}_segment_{}.png'.format(agent, scen, segment), bbox_inches='tight')
    # plt.show()
    plt.close()

def create_combined_plot(data, agent, action, goal):
    data = np.sum(data, axis=0)
    data = normalize(data)
    print("MSE: ", error_analysis(data))
    plt.imshow(data, cmap='viridis')
    # Add text annotations for each pixel
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            plt.text(j, i, str(data[i, j]), ha='center', va='center', color='white')

    plt.xticks(np.arange(5), labels=['1st', '2nd', '3rd', '4th', '5th'])
    plt.yticks(np.arange(5), labels=['up', 'left', 'down', 'right', 'stop'])
    if action == "strict":
        plt.suptitle("Action Ordering Distribution using Strict Ordering")
    else:
        plt.suptitle("Action Ordering Distribution using Sampled Ordering")

    plt.colorbar()

    plt.savefig('action_viz_' + action + goal + '/num_agents_{}_scen_{}_combined.png'.format(agent, scen), dpi=300, bbox_inches='tight')
    # plt.show()
    plt.close()



for agent in num_agents:
    action_type = ["strict", "random"]
    goal_type = ["_no_goal", ""]
    for a in action_type:
        for g in goal_type:
            data = np.load("action_distribution_" + a + g + f"/agent_{agent}_scen_{scen}.npy")
    # for batch in range(int(len(data_strict) / (rows * cols))):
    #     starting_timestep = batch * rows * cols
        # create_segmented_subplots(data_strict[starting_timestep:starting_timestep + rows * cols], batch)
            create_combined_plot(data, agent, a, g)
