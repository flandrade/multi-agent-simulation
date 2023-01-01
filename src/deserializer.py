import json

class SimulationConfig(object):
  def __init__(self, simulation):
    self.name = simulation.get('name')
    self.steps = simulation.get('steps')
    self.territory = TerritoryConfig(**simulation.get('territory'))

  def __str__(self):
    return "Simulation\n Name: {0} | Steps: {1}\n {2}".format(self.name, self.steps, self.territory)

class TerritoryConfig(object):
  def __init__(self, width, height, coordinates):
    self.width = width
    self.height = height

  def __str__(self):
    return "Territory\n  Width: {0} | Height: {1}".format(self.width, self.height)

class CoordinatesConfig(object):
  def __init__(self, defaultProperties, configuration):
    self.default_properties = defaultProperties
    self.configuration = configuration

class CoordinateConfig(object):
  def __init__(self, x, y, properties):
    self.x = x
    self.y = y
    self.properties = properties

class CoordinatePropertiesConfig(object):
  def __init__(self, name, value):
    self.name = name
    self.value = value

if __name__ == '__main__':
  with open('config/ant-colony.json') as config_file:
    conf = config_file.read()

  parsed_json = json.loads(conf)
  sim = SimulationConfig(**parsed_json)
  print(sim)
