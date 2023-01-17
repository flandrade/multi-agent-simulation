"""
Transform JSON file to .mas

"""

import json
from deserializer import simulation_from_dict

def ident(number):
    return " "*number*4

def main():
    # open the JSON file and read the contents
    with open('config/ant-colony.json') as config_file:
        conf = config_file.read()
    config = simulation_from_dict(json.loads(conf))

    print(f'{ident(0)}name: "{config.simulation.name}"')
    print(f'{ident(0)}steps: {config.simulation.steps}')

    print(f'{ident(0)}territory:')
    print(f'{ident(1)}width: {config.simulation.territory.width}')
    print(f'{ident(1)}height: {config.simulation.territory.height}')
    print(f'{ident(1)}coordinates:')
    if config.simulation.territory.default_coordinate is not None:
        coord = config.simulation.territory.default_coordinate
        print(f'{ident(2)}Coordinate x: {coord.x} y: {coord.y}')
        print(f'{ident(3)}properties:')
        for prop in coord.properties:
                print(f'{ident(4)}TerritoryProperty name: "{prop.name}" value: {prop.value} isDefault: true')
    if config.simulation.territory.coordinates is not None:
        for coord in config.simulation.territory.coordinates:
            print(f'{ident(2)}Coordinate x: {coord.x} y: {coord.y}')
            print(f'{ident(3)}properties:')
            for prop in coord.properties:
                print(f'{ident(4)}TerritoryProperty name: "{prop.name}" value: {prop.value} isDefault: false')

    print(f'{ident(0)}agents:')
    for agent in config.simulation.agents:
        print(f'{ident(1)}Agent name: "{agent.name}" type: "{agent.type}"')
        print(f'{ident(2)}locatedAt:')
        print(f'{ident(3)}Coordinate x: {agent.located_at.x} y: {agent.located_at.y}')
        print(f'{ident(2)}properties:')
        for prop in agent.properties:
            # define property that show liveness (that means: if agent is live or present in the grid)
            temp_liveness_property = [pr for pr in config.simulation.agent_properties if pr.represent_liveness]
            liveness_property = temp_liveness_property[0].name if len(temp_liveness_property) > 0 else None
            print(f'{ident(3)}AgentProperty name: "{prop.name}" value: {prop.value} representLiveness: {"true" if prop.name == liveness_property else "false"}')

    print(f'{ident(0)}agentRules:')
    for rule in config.simulation.agent_rules:
        print(f'{ident(1)}AgentRule name: "{rule.name}" type: "{rule.type}"')
        print(f'{ident(2)}description: "{rule.description}"')
        print(f'{ident(2)}preconditions:')
        for precondition in rule.preconditions:
            print(f'{ident(3)}Precondition identifier: "{precondition.identifier.value}"')
            print(f'{ident(4)}optionsString:')
            options = filter(lambda a: not a.startswith('__'), dir(precondition.options))
            for key in options:
                attribute_value = getattr(precondition.options, key)
                if(isinstance(getattr(precondition.options, key), str)):
                    print(f'{ident(5)}Option name: "{key}" value: "{attribute_value}"')

            print(f'{ident(4)}optionsInt:')
            options = filter(lambda a: not a.startswith('__'), dir(precondition.options))
            for key in options:
                attribute_value = getattr(precondition.options, key)
                if(isinstance(getattr(precondition.options, key), int)):
                    print(f'{ident(5)}Option name: "{key}" value: {attribute_value}')

        print(f'{ident(2)}postconditions:')
        for precondition in rule.postconditions:
            print(f'{ident(3)}Postcondition identifier: "{precondition.identifier.value}"')
            print(f'{ident(4)}optionsString:')
            options = filter(lambda a: not a.startswith('__'), dir(precondition.options))
            for key in options:
                attribute_value = getattr(precondition.options, key)
                if(isinstance(getattr(precondition.options, key), str)):
                    print(f'{ident(5)}Option name: "{key}" value: "{attribute_value}"')

            print(f'{ident(4)}optionsInt:')
            options = filter(lambda a: not a.startswith('__'), dir(precondition.options))
            for key in options:
                attribute_value = getattr(precondition.options, key)
                if(isinstance(getattr(precondition.options, key), int)):
                    print(f'{ident(5)}Option name: "{key}" value: {attribute_value}')


    print(f'{ident(0)}territoryRules:')
    for rule in config.simulation.territory_rules:
        print(f'{ident(1)}TerritoryRule name: "{rule.name}"')
        print(f'{ident(2)}description: "{rule.description}"')
        print(f'{ident(2)}preconditions:')
        for precondition in rule.preconditions:
            print(f'{ident(3)}Precondition identifier: "{precondition.identifier.value}"')
            print(f'{ident(4)}optionsString:')
            options = filter(lambda a: not a.startswith('__'), dir(precondition.options))
            for key in options:
                attribute_value = getattr(precondition.options, key)
                if(isinstance(getattr(precondition.options, key), str)):
                    print(f'{ident(5)}Option name: "{key}" value: "{attribute_value}"')

            print(f'{ident(4)}optionsInt:')
            options = filter(lambda a: not a.startswith('__'), dir(precondition.options))
            for key in options:
                attribute_value = getattr(precondition.options, key)
                if(isinstance(getattr(precondition.options, key), int)):
                    print(f'{ident(5)}Option name: "{key}" value: {attribute_value}')

        print(f'{ident(2)}postconditions:')
        for precondition in rule.postconditions:
            print(f'{ident(3)}Postcondition identifier: "{precondition.identifier.value}"')
            print(f'{ident(4)}optionsString:')
            options = filter(lambda a: not a.startswith('__'), dir(precondition.options))
            for key in options:
                attribute_value = getattr(precondition.options, key)
                if(isinstance(getattr(precondition.options, key), str)):
                    print(f'{ident(5)}Option name: "{key}" value: "{attribute_value}"')

            print(f'{ident(4)}optionsInt:')
            options = filter(lambda a: not a.startswith('__'), dir(precondition.options))
            for key in options:
                attribute_value = getattr(precondition.options, key)
                if(isinstance(getattr(precondition.options, key), int)):
                    print(f'{ident(5)}Option name: "{key}" value: {attribute_value}')

if __name__ == '__main__':
    main()
