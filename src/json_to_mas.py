"""
Transform JSON file to .mas, this helps to manually "golden test" our JSON files
It's ugly, I know, we shouldn't include in the project assets
"""

import json
from deserializer import simulation_from_dict
import enum

def ident(number):
    return " "*number*4

string_options = {
    'property_agent': 'propertyAgent',
    'property_territory': 'propertyTerritory',
    'compare': 'compare',
    'agent_type': 'agentType',
    'value_type': 'valueType',
    'direction': 'direction',
    'affected': 'affected',
    'type': 'optionType'
}

int_options = {
    'threshold': 'optionThreshold',
    'value': 'optionValue',
    'probability_of_changing': 'probabilityOfChanging',
    'probability_of_Adding': 'probabilityOfAdding',
    'turn_degrees': 'turnDegrees',
    'amount': 'amount'
}

def get_condition(name):
    if name in int_options:
        return int_options.get(name)
    elif name in string_options:
        return string_options.get(name)
    else:
        return f'"{name}"'

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
        print(f'{ident(3)}coordinateProperties:')
        for prop in coord.properties:
                print(f'{ident(4)}TerritoryProperty "{prop.name}" value: {prop.value} isDefault: true')
    if config.simulation.territory.coordinates is not None:
        for coord in config.simulation.territory.coordinates:
            print(f'{ident(2)}Coordinate x: {coord.x} y: {coord.y}')
            print(f'{ident(3)}coordinateProperties:')
            for prop in coord.properties:
                print(f'{ident(4)}TerritoryProperty "{prop.name}" value: {prop.value} isDefault: false')

    print(f'{ident(0)}agents:')
    for agent in config.simulation.agents:
        print(f'{ident(1)}Agent "{agent.name}" type: "{agent.type}"')
        print(f'{ident(2)}locatedAt:')
        print(f'{ident(3)}Coordinate x: {agent.located_at.x} y: {agent.located_at.y}')
        print(f'{ident(2)}agentProperties:')
        for prop in agent.properties:
            print(f'{ident(3)}AgentProperty "{prop.name}" value: {prop.value} representLiveness: {"true" if prop.represent_liveness else "false"}')

    print(f'{ident(0)}agentRules:')
    for rule in config.simulation.agent_rules:
        print(f'{ident(1)}AgentRule "{rule.name}" type: "{rule.type}"')
        print(f'{ident(2)}description: "{rule.description}"')
        print(f'{ident(2)}preconditions:')
        for precondition in rule.preconditions:
            print(f'{ident(3)}Condition "{precondition.identifier.value}"')
            print(f'{ident(4)}optionsString:')
            options = filter(lambda a: not a.startswith('__'), dir(precondition.options))
            for key in options:
                attribute_value = getattr(precondition.options, key)
                if key in string_options and attribute_value is not None:
                    print(f'{ident(5)}Option {get_condition(key)} value: "{attribute_value.value if isinstance(attribute_value, enum.Enum) else attribute_value}"')

            print(f'{ident(4)}optionsInt:')
            options = filter(lambda a: not a.startswith('__'), dir(precondition.options))
            for key in options:
                attribute_value = getattr(precondition.options, key)
                if key in int_options and attribute_value is not None:
                    print(f'{ident(5)}Option {get_condition(key)} value: {int(attribute_value)}')

        print(f'{ident(2)}postconditions:')
        for precondition in rule.postconditions:
            print(f'{ident(3)}Condition "{precondition.identifier.value}"')
            print(f'{ident(4)}optionsString:')
            options = filter(lambda a: not a.startswith('__'), dir(precondition.options))
            for key in options:
                attribute_value = getattr(precondition.options, key)
                if key in string_options and attribute_value is not None:
                    print(f'{ident(5)}Option {get_condition(key)} value: "{attribute_value.value if isinstance(attribute_value, enum.Enum) else attribute_value}"')

            print(f'{ident(4)}optionsInt:')
            options = filter(lambda a: not a.startswith('__'), dir(precondition.options))
            for key in options:
                attribute_value = getattr(precondition.options, key)
                if key in int_options and attribute_value is not None:
                    print(f'{ident(5)}Option {get_condition(key)} value: {int(attribute_value)}')


    print(f'{ident(0)}territoryRules:')
    for rule in config.simulation.territory_rules:
        print(f'{ident(1)}TerritoryRule "{rule.name}"')
        print(f'{ident(2)}description: "{rule.description}"')
        print(f'{ident(2)}preconditions:')
        for precondition in rule.preconditions:
            print(f'{ident(3)}Condition "{precondition.identifier.value}"')
            print(f'{ident(4)}optionsString:')
            options = filter(lambda a: not a.startswith('__'), dir(precondition.options))
            for key in options:
                attribute_value = getattr(precondition.options, key)
                if key in string_options and attribute_value is not None:
                    print(f'{ident(5)}Option {get_condition(key)} value: "{attribute_value.value if isinstance(attribute_value, enum.Enum) else attribute_value}"')

            print(f'{ident(4)}optionsInt:')
            options = filter(lambda a: not a.startswith('__'), dir(precondition.options))
            for key in options:
                attribute_value = getattr(precondition.options, key)
                if key in int_options and attribute_value is not None:
                    print(f'{ident(5)}Option {get_condition(key)} value: {int(attribute_value)}')

        print(f'{ident(2)}postconditions:')
        for precondition in rule.postconditions:
            print(f'{ident(3)}Condition "{precondition.identifier.value}"')
            print(f'{ident(4)}optionsString:')
            options = filter(lambda a: not a.startswith('__'), dir(precondition.options))
            if key in string_options and attribute_value is not None:
                print(f'{ident(5)}Option {get_condition(key)} value: "{attribute_value.value if isinstance(attribute_value, enum.Enum) else attribute_value}"')

            print(f'{ident(4)}optionsInt:')
            options = filter(lambda a: not a.startswith('__'), dir(precondition.options))
            for key in options:
                attribute_value = getattr(precondition.options, key)
                if key in int_options and attribute_value is not None:
                    print(f'{ident(5)}Option {get_condition(key)} value: {int(attribute_value)}')

if __name__ == '__main__':
    main()
