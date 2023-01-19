import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

_g = globals()
scats = []

def define_scat(agent_types, agents, step, liveness_property):
    types = []
    for type in agent_types:
        ag_set = [ag for ag in agents[step] if ag.type == type]
        list = []
        for ag in [ag for ag in ag_set]:
            ag_location = ag.location
            # only plot alive agents
            if (liveness_property is None or ag.properties[liveness_property] == 1):
                alive_agents_location_x = ag_location[0]
                alive_agents_location_y = ag_location[1]
                list.append((alive_agents_location_x, alive_agents_location_y))
        types.append(list)
    return types

def plot_simulation(agent_types, name, territory_size, data, liveness_property):
    agent_colors = np.random.rand(len(agent_types), 3)
    # extract the x and y values for the plot
    steps, territory, agents = zip(*data)
    # setup animation
    fig, ax = plt.subplots()
    ax.set_xlim([-1, territory_size[0]])
    ax.set_ylim([-1, territory_size[1]])

    # to remove dead agents:
    # https://stackoverflow.com/questions/43074828/remove-precedent-scatterplot-while-updating-python-animation
    def update(frame):
        global scats
        # first remove all old scatters
        for scat in scats:
            scat.remove()
        scats=[]
        new_values = define_scat(agent_types, agents, frame, liveness_property)
        for index, value in enumerate(new_values):
            if len(value) > 0:
                x = [i[0] for i in value]
                y = [i[1] for i in value]
                scats.append(ax.scatter(x, y, s=150, marker=(5, 1), color=agent_colors[index].reshape(1,-1)))
                legend1 = ax.legend(agent_types, loc="upper right", title="Agents")
                ax.add_artist(legend1)


    ani = FuncAnimation(fig, update, frames=steps, repeat=False, interval=220)

    plt.grid()
    plt.title(name, fontsize = 18)
    plt.show()
