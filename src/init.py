import json
import pprint

from deserializer import simulation_from_dict

if __name__ == '__main__':
    with open('config/ant-colony.json') as config_file:
        conf = config_file.read()

    config = simulation_from_dict(json.loads(conf))
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(config.to_dict())
