import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

_g = globals()

def define_scat(agent_types, agents, step, liveness_property):
    types = []
    for type in agent_types:
        ag_set = [ag for ag in agents[step] if ag.type == type]
        list = []
        for ag in [ag for ag in ag_set]:
            ag_location = ag.location
            # only plot alive agents
            if (ag.properties[liveness_property] == 1):
                alive_agents_location_x = ag_location[0]
                alive_agents_location_y = ag_location[1]
                list.append((alive_agents_location_x, alive_agents_location_y))
        types.append(list)
    return types

def plot_simulation(types, name, territory_size, data, liveness_property):
    agent_types = [ag.name for ag in types]
    agent_colors = np.random.rand(len(agent_types), 3)
    # extract the x and y values for the plot
    steps, territory, agents = zip(*data)
    # setup animation
    fig, ax = plt.subplots()
    ax.set_xlim([-1, territory_size[0]])
    ax.set_ylim([-1, territory_size[1]])

    data_per_agent_type = define_scat(agent_types, agents, 0, liveness_property)
    for index, value in enumerate(data_per_agent_type):
        x = [i[0] for i in value]
        y = [i[1] for i in value]
        _g[f'scat_{index}'] = ax.scatter(x, y, s=150, marker=(5, 1), color=agent_colors[index].reshape(1,-1))

    def update(frame):
        new_values = define_scat(agent_types, agents, frame, liveness_property)
        for index, value in enumerate(new_values):
            if len(value) > 0:
                _g[f'scat_{index}'].set_offsets(value)
                return _g[f'scat_{index}'],

    ani = FuncAnimation(fig, update, frames=range(1, len(steps)-1), repeat=False, interval=200)

    plt.grid()
    plt.title(name, fontsize = 18)
    plt.show()
