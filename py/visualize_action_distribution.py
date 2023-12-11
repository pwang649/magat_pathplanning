import numpy as np
import matplotlib.pyplot as plt

# Arguments
rows = 3
cols = 4
num_agents = 100
scen = 1
LaCAM_shielding = False


path_postfix = "_LaCAM" if LaCAM_shielding else ""

def create_segmented_subplots(data, segment):
    fig, axs = plt.subplots(rows, cols)

    for i, ax in enumerate(axs.flatten()):
        if i < len(data):
            img = ax.imshow(data[i])
        else:
            ax.remove()
    stopping_timestep = starting_timestep + rows * cols - 1
    plt.suptitle(f'num_agents: {num_agents}, scen: {scen}, timestep: {starting_timestep} to {stopping_timestep}')
    cbar = fig.colorbar(img, ax=axs, fraction=0.02, pad=0.04)
    plt.savefig('action_distribution_visualizations' + path_postfix + '/num_agents_{}_scen_{}_segment_{}.png'.format(num_agents, scen, segment), bbox_inches='tight')
    # plt.show()

data = np.load("action_distribution" + path_postfix + f"/agent_{num_agents}_scen_{scen}.npy")
for batch in range(int(len(data) / (rows * cols))):
    starting_timestep = batch * rows * cols
    create_segmented_subplots(data[starting_timestep:starting_timestep + rows * cols], batch)
