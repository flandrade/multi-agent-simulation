# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 16:12:35 2022

@author: Grandury
"""
import copy
import json
import numpy as np
import random
from plot import plot_simulation
import uuid
from deserializer import simulation_from_dict, Condition, Compare, Action, UpdateType, DirectionType
from utils import normalize

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
                if precondition.condition == Condition.COMPARE_PROPERTY:
                    options = precondition.options
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
                    elif options.compare == Compare.LESS_THAN:
                        preconditions_satisfied.append(value == options.threshold)
                # add other conditions as needed

            # if all the preconditions are satisfied, apply the postconditions
            if all(preconditions_satisfied) and len(preconditions_satisfied) > 0:
                for postcondition in rule.postconditions:
                    options = postcondition.options
                    if postcondition.action == Action.MOVE:
                        if options.direction == DirectionType.RANDOM:
                            new_x = normalize(copy.deepcopy(self.location[0]) + random.randint(-1, 1), 0, territory.size[1] - 1)
                            new_y = normalize(copy.deepcopy(self.location[1]) + random.randint(-1, 1), 0, territory.size[1] - 1)
                            self.location = (new_x, new_y)
                    if postcondition.action == Action.CHANGE_PROPERTY:
                        if options.property_agent is not None:
                            prev = self.properties[options.property_agent]
                            # change a property of the agent
                            if options.update_type == UpdateType.INCREASE:
                                # is it's same agent
                                if options.affected is None:
                                    self.properties[options.property_agent] = prev + options.value
                                # if it's different agent
                                elif options.affected is not None and len(agents_in_same_location) > 0:
                                    agents_in_same_location[0].properties[options.property_agent] += options.value
                            elif options.update_type == UpdateType.DECREASE:
                                # is it's same agent
                                if options.affected is None:
                                    self.properties[options.property_agent] = prev - options.value
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

                    # should be here to avoid overlapping
                    if postcondition.action == Action.INTRODUCE_AGENTS:
                        return options
        return None

class Territory:
    def __init__(self, territory):
        self.size = (territory.width, territory.height)
        # extract the territory coordinates and their properties from the JSON file
        territory_properties = {}
        coord_properties = {}
        for prop in territory.coordinates.default_properties:
            coord_properties[prop.name] = prop.value
        for i in range (0, self.size[0]):
            for j in range (0, self.size[1]):
                territory_properties[(i, j)] = coord_properties
        for coord_data in territory.coordinates.configuration:
            coord_properties = {}
            for prop in coord_data.properties:
                coord_properties[prop.name] = prop.value
            territory_properties[(coord_data.x, coord_data.y)] = coord_properties
        self.coordinates = territory_properties

    def apply_evolution_rules(self):
        # implement the logic for applying the evolution rules for the territory
        pass

def simulate(agents, territory, steps, rules):
    new_data = []
    new_data.append((0, territory, copy.deepcopy(agents)))
    for i in range(1, steps):
        # iterate through agents to apply rules
        for agent in agents:
            # get agents in same location different from the agent
            agents_in_same_location = [ag for ag in agents if ag.location == agent.location and ag.name != agent.name]
            result = agent.apply_behavior_rules(rules, territory, agents_in_same_location)
            # if rule returns value, new agent should be created.
            # NOTE: name should be unique
            if result is not None:
                new_agent = Agent(str(uuid.uuid4()), result.agent_type, agent.location, get_agent_properties(result.properties))
                agents.append(new_agent)
            # apply the evolution rules for the territory
        territory.apply_evolution_rules()
        this_agents = copy.deepcopy(agents)
        this_territory = copy.deepcopy(territory)
        #print("----")
        #print(territory.coordinates)
        # collect data for the plot
        new_data.append((i, this_territory, this_agents))
    return new_data

def get_agent_properties(properties):
    agent_properties = {}
    for prop in properties:
        agent_properties[prop.name] = prop.value
    return agent_properties

def main():
    # open the JSON file and read the contents
    with open('config/ant-colony.json') as config_file:
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
    data = simulate(agents, territory, config.simulation.steps, config.simulation.agent_rules)

    # define property that show liveness (that means: if agent is live or present in the grid)
    temp_liveness_property = [pr for pr in config.simulation.agent_properties if pr.represent_liveness]
    liveness_property = temp_liveness_property[0].name if len(temp_liveness_property) > 0 else None

    for step in data:
        print(f'step {step[0]}')
        for ag in step[2]:
            print(f'{ag.location} {ag.type} {ag.properties}')

    # plot
    plot_simulation(config.simulation.agent_type, config.simulation.name, territory.size, data, liveness_property)

if __name__ == '__main__':
    main()
