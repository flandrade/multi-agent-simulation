import copy
import json
import sys
import random
from plot import plot_simulation
import uuid
from deserializer import simulation_from_dict, Condition, Compare, Action, UpdateType, DirectionType, PurpleOptions
from utils import normalize, decision

class Agent:
    def __init__(self, name, type, location, properties):
        self.name = name
        self.type = type
        self.location = location
        self.properties = properties


    def apply_behavior_rules(self, rules, territory, agents_in_same_location=[]):
        """
        Apply behavior rules to agent. Returns TRUE if new agent should be created
        """
        # filter rules for agent type
        filtered_rules = [rul for rul in rules if rul.type == self.type]
        # coordinates
        coordinate = territory.coordinates[self.location]
        # apply each behavior rule in turn
        for rule in filtered_rules:
            # check if the preconditions are satisfied
            preconditions_satisfied = []
            for precondition in rule.preconditions:
                options = precondition.options
                if precondition.identifier == Condition.CHECK_PRESENCE:
                    presence = [ag for ag in agents_in_same_location if ag.type == options.type]
                    if options.value == 0:
                        preconditions_satisfied.append(len(presence) == options.value)
                    else:
                        preconditions_satisfied.append(len(presence) >= options.value)
                if precondition.identifier == Condition.COMPARE_PROPERTY:
                    if options.property_agent is not None:
                        # compare a property of the agent
                        value = self.properties[options.property_agent]
                    else:
                        # compare a property of the territory
                        value = coordinate[options.property_territory]
                    if options.compare == Compare.GREATER_THAN:
                        preconditions_satisfied.append(value > options.threshold)
                    elif options.compare == Compare.LESS_THAN:
                        preconditions_satisfied.append(value < options.threshold)
                    elif options.compare == Compare.EQUAL:
                        preconditions_satisfied.append(value == options.threshold)
                # add other conditions as needed

            # if all the preconditions are satisfied, apply the postconditions
            if all(preconditions_satisfied) and len(preconditions_satisfied) > 0:
                print(f'Agent Rule - [{self.name[0:2]}|{self.type}] at {self.location}. Execute rule: {rule.name}')
                for postcondition in rule.postconditions:
                    options = postcondition.options
                    if postcondition.identifier == Action.MOVE:

                        if options.direction == DirectionType.RANDOM:
                            new_x = normalize(copy.deepcopy(self.location[0]) + random.randint(-1, 1), 0, territory.size[1] - 1)
                            new_y = normalize(copy.deepcopy(self.location[1]) + random.randint(-1, 1), 0, territory.size[1] - 1)
                            self.location = (new_x, new_y)

                        elif options.direction == DirectionType.PROPERTY:
                            row = self.location[0]
                            col = self.location[1]
                            maximum = (row, col)

                            pheromones_max = territory.coordinates[maximum][options.property_territory]

                            for pos in ( (row - 1, col), (row + 1, col), (row, col - 1),
                                       (row, col + 1), (row - 1, col - 1), (row - 1, col + 1),
                                       (row + 1, col - 1), (row + 1, col + 1)):

                                pheromones = 0
                                for coord in territory.coordinates:
                                    if (coord[0] == pos[0] and coord[1] == pos[1]):
                                        for prop1 in territory.coordinates[coord]:
                                            if prop1 == options.property_territory:
                                                pheromones = territory.coordinates[coord][options.property_territory]

                                if pheromones > pheromones_max:
                                    pheromones_max = pheromones
                                    maximum = (pos[0],pos[1])

                            self.location = (maximum[0], maximum[1])

                    if postcondition.identifier == Action.CHANGE_PROPERTY:
                        if options.property_agent is not None and decision(options.probability_of_changing):
                            # change a property of the agent
                            if options.update_type == UpdateType.INCREASE:
                                # is it's same agent
                                if options.affected is None:
                                    prev = self.properties[options.property_agent]
                                    self.properties[options.property_agent] = prev + options.value
                                # if it's different agent
                                elif options.affected is not None and len(agents_in_same_location) > 0:
                                    agents_in_same_location[0].properties[options.property_agent] += options.value
                            elif options.update_type == UpdateType.DECREASE:
                                # is it's same agent
                                if options.affected is None:
                                    prev = self.properties[options.property_agent]
                                    self.properties[options.property_agent] = prev - options.value
                                # if it's different agent
                                elif options.affected is not None and len(agents_in_same_location) > 0:
                                    agents_in_same_location[0].properties[options.property_agent] -= options.value
                            elif options.update_type == UpdateType.UPDATE:
                                # is it's same agent
                                if options.affected is None:
                                    prev = self.properties[options.property_agent]
                                    self.properties[options.property_agent] = options.value
                                # if it's different agent
                                elif options.affected is not None and len(agents_in_same_location) > 0:
                                    agents_in_same_location[0].properties[options.property_agent] = options.value
                        else:
                            # change a property of the territory
                            if options.update_type == UpdateType.INCREASE and decision(options.probability_of_changing):
                                coordinate[options.property_territory] += options.value

                    # should be here to avoid overlapping
                    # since creating an agent is independent of this agent, we return a data structure with the new agent
                    # properties, and the simulate function will create the new agent
                    if postcondition.identifier == Action.INTRODUCE_AGENTS:
                        if decision(options.probability_of_adding):
                            return options
                        else:
                            pass
        return None

class Territory:
    def __init__(self, territory):
        self.size = (territory.width, territory.height)
        # extract the territory coordinates and their properties from the JSON file
        territory_properties = {}
        if territory.default_coordinate.properties is not None:
            coord_properties = {}
            for prop in territory.default_coordinate.properties:
                coord_properties[prop.name] = prop.value

            for i in range (0, self.size[0]):
                for j in range (0, self.size[1]):
                    territory_properties[(i, j)] = copy.deepcopy(coord_properties)

        if territory.coordinates is not None:
            for coord_data in territory.coordinates:
                coord_properties = {}
                for prop in coord_data.properties:
                    coord_properties[prop.name] = prop.value
                territory_properties[(coord_data.x, coord_data.y)] = copy.deepcopy(coord_properties)

        self.coordinates = territory_properties


    def apply_evolution_rules(self, rules):
        # implement the logic for applying the evolution rules for the territory
        # apply each behavior rule in turn
        for rule in rules:
            for coord in self.coordinates:
                preconditions_satisfied = []
                for precondition in rule.preconditions:
                    options = precondition.options
                    if precondition.identifier == Condition.COMPARE_PROPERTY:
                        value = self.coordinates[coord][options.property_territory]
                        if options.compare == Compare.GREATER_THAN:
                            preconditions_satisfied.append(value > options.threshold)

                        if all(preconditions_satisfied) and len(preconditions_satisfied) > options.threshold:
                            # print(f'Territory Rule - [{coord}]. Execute rule: {rule.name}')
                            for postcondition in rule.postconditions:
                                options = postcondition.options
                                if postcondition.identifier == Action.CHANGE_PROPERTY:
                                    prev = self.coordinates[coord][options.property_territory]
                                    self.coordinates[coord][options.property_territory] = prev - options.value



def simulate(agents, territory, steps, agent_rules, territory_rules):
    new_data = []
    new_data.append((0, copy.deepcopy(territory), copy.deepcopy(agents)))

    print (f'-------------- RULES LOG --------------')
    for i in range(1, steps):
        print (f'STEP {i}-------')
        # iterate through agents to apply rules
        for agent in agents:
            # get agents in same location different from the agent
            agents_in_same_location = [ag for ag in agents if ag.location == agent.location and ag.name != agent.name]
            result = agent.apply_behavior_rules(agent_rules, territory, agents_in_same_location)
            # if rule returns value, new agent should be created.
            # NOTE: name should be unique
            if result is not None:
                props = get_agent_properties(result.properties, agents, result.agent_type)
                new_agent = Agent(str(uuid.uuid4()), result.agent_type, agent.location, props)
                agents.append(new_agent)
            # apply the evolution rules for the territory
        territory.apply_evolution_rules(territory_rules)
        this_agents = copy.deepcopy(agents)
        this_territory = copy.deepcopy(territory)

        # collect data for the plot
        new_data.append((i, this_territory, this_agents))
    return new_data


def get_agent_properties(properties, agents=None, type=None):
    agent_properties = {}
    if properties is None:
        aux = filter(lambda a: a.type == type, agents)
        return next(aux).properties

    for prop in properties:
        agent_properties[prop.name] = prop.value
    return agent_properties


def main():
    # open the JSON file and read the contents
    with open(sys.argv[1]) as config_file:
        conf = config_file.read()
    config = simulation_from_dict(json.loads(conf))

    # extract the agents and their properties from the JSON file
    agents = []
    for agent_data in config.simulation.agents:
        agent_properties = get_agent_properties(agent_data.properties)
        agent = Agent(agent_data.name, agent_data.type, (agent_data.located_at.x, agent_data.located_at.y), agent_properties)
        agents.append(agent)

    # create the territory with the extracted data
    territory = Territory(config.simulation.territory)
    # run the simulation and collect the data
    data = simulate(agents, territory, config.simulation.steps, config.simulation.agent_rules, config.simulation.territory_rules)

    # define property that show liveness (that means: if agent is live or present in the grid)
    liveness_property = None
    for agent in config.simulation.agents:
        for property in agent.properties:
            if property.represent_liveness:
                liveness_property = property.name
                break
    # define agent types, we use a set to avoid repeated elements
    agent_types = set([])
    for agent in agents:
        agent_types.add(agent.type)

    print (f'-------------- AGENT/TERRITORY STATE LOG --------------')
    for step in data:
        print (f'STEP {step[0]}-------')
        print(f'{step[1].coordinates}')
        for ag in step[2]:
            print(f'{ag.location} {ag.type} {ag.properties}')

    # plot
    plot_simulation(list(agent_types), config.simulation.name, territory.size, data, liveness_property)

if __name__ == '__main__':
    main()
