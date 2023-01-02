from matplotlib import pyplot

def plot_simulation(types, name, territory_size, data):
    agent_types = [ag.name for ag in types]
    # extract the x and y values for the plot
    steps, territory, agents = zip(*data)
    step=0
    for type in agent_types:
        ag_set = [ag for ag in agents[step] if ag.type == type]
        alive_agents_location_x = [ag.location[0] for ag in ag_set]
        alive_agents_location_y = [ag.location[1] for ag in ag_set]
        pyplot.scatter(alive_agents_location_x, alive_agents_location_y, s=150, marker=(5, 1))

    pyplot.title(name, fontsize = 24)
    pyplot.xticks(range(0, territory_size[0]))
    pyplot.yticks(range(0, territory_size[1]))
    pyplot.grid()
    pyplot.show()
