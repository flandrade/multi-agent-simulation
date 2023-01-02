# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 16:12:35 2022

@author: Grandury
"""
import json
import numpy as np
import random
from plot import plot_simulation
import uuid
from deserializer import simulation_from_dict, Condition, Compare, Action, UpdateType

class Agent:
    def __init__(self, name, type, location, properties):
        self.name = name
        self.type = type
        self.location = location
        self.properties = properties


    def apply_behavior_rules(self, rules, coordinate, agents_in_same_location=[]):
        """
        Apply behavior rules to agent. Returns TRUE if new agent should be created
        """
        # filter rules for agent type
        filtered_rules = [rul for rul in rules if rul.type == self.type]
        # apply each behavior rule in turn
        for rule in filtered_rules:
            # check if the preconditions are satisfied
            preconditions_satisfied = True
            for precondition in rule.preconditions:
                if precondition.condition == Condition.COMPARE_PROPERTY:
                    options = precondition.options
                    if options.property_agent is not None:
                        # compare a property of the agent
                        value = self.properties[options.property_agent]
                    else:
                        # compare a property of the territory
                        value = coordinate[options.property_territory]
                    if options.compare == Compare.GREATER_THAN:
                        preconditions_satisfied = value > options.threshold
                    elif options.compare == Compare.LESS_THAN:
                        preconditions_satisfied = value < options.threshold
                    elif options.compare == Compare.LESS_THAN:
                        preconditions_satisfied = value == options.threshold
                    return False
                # add other conditions as needed

            # if the preconditions are satisfied, apply the postconditions
            if preconditions_satisfied:
                for postcondition in rule.postconditions:
                    if postcondition.action == Action.INTRODUCE_AGENTS:
                        return True
                    if postcondition.action == Action.CHANGE_PROPERTY:
                        options = postcondition.options
                        if options.property_agent is not None:
                            # change a property of the agent
                            if options.update_type == UpdateType.INCREASE:
                                # is it's same agent
                                if options.affected is None:
                                    self.properties[options.property_agent] += options.value
                                # if it's different agent
                                elif options.affected is not None and len(agents_in_same_location) > 0:
                                    agents_in_same_location[0].properties[options.property_agent] += options.value
                            elif options.update_type == UpdateType.DECREASE:
                                # is it's same agent
                                if options.affected is None:
                                    self.properties[options.property_agent] -= options.value
                                # if it's different agent
                                elif options.affected is not None and len(agents_in_same_location) > 0:
                                    agents_in_same_location[0].properties[options.property_agent] -= options.value
                            elif options.update_type == UpdateType.UPDATE:
                                # is it's same agent
                                if options.affected is None:
                                    self.properties[options.property_agent] = options.value
                                # if it's different agent
                                elif options.affected is not None and len(agents_in_same_location) > 0:
                                    agents_in_same_location[0].properties[options.property_agent] = options.value
                        else:
                            # change a property of the territory
                            if options.update_type == UpdateType.INCREASE:
                                coordinate[options.property_territory] += options.value
                        return False

class Territory:
    def __init__(self, size, coordinates):
        self.size = size
        self.coordinates = coordinates

    def apply_evolution_rules(self):
        # implement the logic for applying the evolution rules for the territory
        pass

def simulate(data, agents, territory, steps, rules):
    data = []
    for i in range(steps):
        # choose a random agent and apply its behavior rules
        agent = random.choice(agents)
        # get agents in same location different from the agent
        agents_in_same_location = [ag for ag in agents if ag.location == agent.location and ag.name != agent.name]
        result = agent.apply_behavior_rules(rules, territory.coordinates[agent.location], agents_in_same_location)
        # if rule returns True, new agent should be created.
        # NOTE: name should be unique
        if result:
            new_agent = Agent(str(uuid.uuid4()), agent.type, agent.location, agent.properties)
            agents.append(new_agent)
        # apply the evolution rules for the territory
        territory.apply_evolution_rules()

        # collect data for the plot
        data.append((i, territory.coordinates, agents))
    return data

def main():
    # open the JSON file and read the contents
    with open('config/ant-colony.json') as config_file:
        conf = config_file.read()
    config = simulation_from_dict(json.loads(conf))

    # extract the simulation parameters from the JSON file
    territory_size = (config.simulation.territory.width, config.simulation.territory.height)

    # extract the agents and their properties from the JSON file
    agents = []
    for agent_data in config.simulation.agents:
        agent_properties = {}
        for prop in agent_data.properties:
            agent_properties[prop.name] = prop.value
        agent = Agent(agent_data.name, agent_data.type, (agent_data.located_at.x, agent_data.located_at.y), agent_properties)
        agents.append(agent)

    # extract the territory coordinates and their properties from the JSON file
    territory_properties = {}
    for i in range (0, territory_size[0]):
        for j in range (0, territory_size[1]):
            coord_properties = {}
            for prop in config.simulation.territory.coordinates.default_properties:
                coord_properties[prop.name] = prop.value
            territory_properties[(i, j)] = coord_properties
    for coord_data in config.simulation.territory.coordinates.configuration:
        coord_properties = {}
        for prop in coord_data.properties:
            coord_properties[prop.name] = prop.value
        territory_properties[(coord_data.x, coord_data.y)] = coord_properties

    # create the territory with the extracted data
    territory = Territory(territory_size, territory_properties)

    # run the simulation and collect the data
    data = simulate(config, agents, territory, config.simulation.steps, config.simulation.agent_rules)

    # plot
    plot_simulation(config.simulation.agent_type, config.simulation.name, territory_size, data)


if __name__ == '__main__':
    main()
