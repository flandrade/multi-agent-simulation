from enum import Enum
from dataclasses import dataclass
from typing import Any, Optional, List, TypeVar, Type, Callable, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


class Condition(Enum):
    """
    Preconditions that should be fulfilled in order to execute actions (territory or agents).

    Example:
    - "check-presence" of another agent in order to move
    - "compare-property" of the agent in order to change another property
    - In Conway's, we need to "get-neighbors" and compare their properties in order to decide whether to
    change the agent property
    """
    CHECK_PRESENCE = "check-presence"
    COMPARE_PROPERTY = "compare-property"
    GET_NEIGHBORS = "get-neighbors"


class Action(Enum):
    """
    Actions to be executed by either the agents or the territory

    CHANGE_PROPERTY: change the property of the agent or the territory
    INTRODUCE_AGENTS: add new agents or hatch agents (hatch is used in other frameworks as
    NetLogo https://ccl.northwestern.edu/netlogo/bind/primitive/hatch.html)
    MOVE: move an agent in a defined direction (see DirectionType enum)

    Based on Agentbase (which is inspired in Netlogo)
    https://github.com/wybo/agentbase/blob/master/src/agent.coffee
    """
    CHANGE_PROPERTY = "change-property"
    INTRODUCE_AGENTS = "introduce-agents"
    MOVE = "move"


class UpdateType(Enum):
    """
    Update a property value

    Example:
    - "increase" the energy value if a sheep eats grass
    """
    DECREASE = "decrease"
    INCREASE = "increase"
    UPDATE = "update"

class DirectionType(Enum):
    """
    Direction in which an agent moves

    FREE_RANDOM: An agent moves randomly to a free coordinate
    DEGREES: An agent moves into the degrees direction. Supported: 0, 45, 90, 135, 180, 225, 270 and 315
    PROPERTY: An agent move into the direction of the neighbor with a property that fullfil the condition
    RANDOM: An agent moves randomly

    """
    FREE_RANDOM = "free-random"
    DEGREES = "degrees"
    PROPERTY = "property"
    RANDOM = "random"



class CompareNeighbor(Enum):
    """
    Compare a property of a neighbor

    Example:
    - The neighbor with the "highest" energy property
    """
    HIGHEST = "highest"
    LOWEST = "lowest"


class Compare(Enum):
    """
    Compare a property of an agent or territory

    Example:
    - The coordinate with a property that is "greater-than" 0
    """
    EQUAL = "equal"
    GREATER_THAN = "greater-than"
    LESS_THAN = "less-than"


@dataclass
class AgentProperty:
    name: str
    represent_liveness: bool

    @staticmethod
    def from_dict(obj: Any) -> 'AgentProperty':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        represent_liveness = from_bool(obj.get("representLiveness"))
        return AgentProperty(name, represent_liveness)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["representLiveness"] = from_bool(self.represent_liveness)
        return result


@dataclass
class Property:
    name: str
    value: int

    @staticmethod
    def from_dict(obj: Any) -> 'Property':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        value = from_int(obj.get("value"))
        return Property(name, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["value"] = from_int(self.value)
        return result


@dataclass
class PurpleOptions:
    probability_of_changing: Optional[float] = None
    property_agent: Optional[str] = None
    property_territory: Optional[str] = None
    agent_type: Optional[str] = None
    update_type: Optional[UpdateType] = None
    value: Optional[int] = None
    direction: Optional[DirectionType] = None
    turn_degrees: Optional[int] = None
    affected: Optional[str] = None
    compare: Optional[CompareNeighbor] = None
    amount: Optional[int] = None
    probability_of_adding: Optional[float] = None
    properties: Optional[List[Property]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PurpleOptions':
        assert isinstance(obj, dict)
        probability_of_changing = from_union([from_float, from_none], obj.get("probabilityOfChanging"))
        property_agent = from_union([from_none, from_str], obj.get("propertyAgent"))
        property_territory = from_union([from_none, from_str], obj.get("propertyTerritory"))
        agent_type = from_union([from_str, from_none], obj.get("agentType"))
        update_type = from_union([UpdateType, from_none], obj.get("updateType"))
        value = from_union([from_int, from_none], obj.get("value"))
        direction = from_union([DirectionType, from_none], obj.get("direction"))
        turn_degrees = from_union([from_int, from_none], obj.get("turnDegrees"))
        affected = from_union([from_str, from_none], obj.get("agentType"))
        compare = from_union([CompareNeighbor, from_none], obj.get("compare"))
        amount = from_union([from_int, from_none], obj.get("amount"))
        probability_of_adding = from_union([from_float, from_none], obj.get("probabilityOfAdding"))
        properties = from_union([lambda x: from_list(Property.from_dict, x), from_none], obj.get("properties"))
        return PurpleOptions(probability_of_changing, property_agent, property_territory, agent_type, update_type, value, direction, turn_degrees, affected, compare, amount, probability_of_adding, properties)

    def to_dict(self) -> dict:
        result: dict = {}
        result["probabilityOfChanging"] = from_union([from_float, from_none], self.probability_of_changing)
        result["propertyAgent"] = from_union([from_none, from_str], self.property_agent)
        result["propertyTerritory"] = from_union([from_none, from_str], self.property_territory)
        result["agent_type"] = from_union([from_str, from_none], self.agent_type)
        result["update_type"] = from_union([lambda x: to_enum(UpdateType, x), from_none], self.update_type)
        result["value"] = from_union([from_int, from_none], self.value)
        result["direction"] = from_union([lambda x: to_enum(DirectionType, x), from_none], self.direction)
        result["turnDegrees"] = from_union([from_int, from_none], self.turn_degrees)
        result["agentType"] = from_union([from_str, from_none], self.affected)
        result["compare"] = from_union([lambda x: to_enum(CompareNeighbor, x), from_none], self.compare)
        result["amount"] = from_union([from_int, from_none], self.amount)
        result["probabilityOfAdding"] = from_union([from_float, from_none], self.probability_of_adding)
        result["properties"] = from_union([lambda x: from_list(lambda x: to_class(Property, x), x), from_none], self.properties)
        return result


@dataclass
class RulePoscondition:
    identifier: Action
    options: PurpleOptions

    @staticmethod
    def from_dict(obj: Any) -> 'RulePoscondition':
        assert isinstance(obj, dict)
        identifier = Action(obj.get("identifier"))
        options = PurpleOptions.from_dict(obj.get("options"))
        return RulePoscondition(identifier, options)

    def to_dict(self) -> dict:
        result: dict = {}
        result["identifier"] = to_enum(Action, self.action)
        result["options"] = to_class(PurpleOptions, self.options)
        return result


@dataclass
class FluffyOptions:
    property_agent: Optional[str] = None
    property_territory: Optional[str] = None
    compare: Optional[Compare] = None
    threshold: Optional[int] = None
    type: Optional[str] = None
    value: Optional[int] = None
    compare_amount_agents_high: Optional[Compare] = None
    threshold_amount_agents_high: Optional[int] = None
    compare_amount_agents_low: Optional[Compare] = None
    threshold_amount_agents_low: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'FluffyOptions':
        assert isinstance(obj, dict)
        property_agent = from_union([from_none, from_str], obj.get("propertyAgent"))
        property_territory = from_union([from_none, from_str], obj.get("propertyTerritory"))
        compare = from_union([Compare, from_none], obj.get("compare"))
        threshold = from_union([from_int, from_none], obj.get("threshold"))
        type = from_union([from_str, from_none], obj.get("agentType"))
        value = from_union([from_int, from_none], obj.get("value"))
        compare_amount_agents_high = from_union([from_str, from_none], obj.get("compareAmountAgentsHigh"))
        threshold_amount_agents_high = from_union([from_int, from_none], obj.get("thresholdAmountAgentsHigh"))
        compare_amount_agents_low = from_union([from_str, from_none], obj.get("compareAmountAgentsLow"))
        threshold_amount_agents_low = from_union([from_int, from_none], obj.get("thresholdAmountAgentsLow"))
        return FluffyOptions(property_agent, property_territory, compare, threshold, type, value, compare_amount_agents_high, threshold_amount_agents_high, compare_amount_agents_low, threshold_amount_agents_low)

    def to_dict(self) -> dict:
        result: dict = {}
        result["propertyAgent"] = from_union([from_none, from_str], self.property_agent)
        result["propertyTerritory"] = from_union([from_none, from_str], self.property_territory)
        result["compare"] = from_union([lambda x: to_enum(Compare, x), from_none], self.compare)
        result["threshold"] = from_union([from_int, from_none], self.threshold)
        result["agentType"] = from_union([from_str, from_none], self.type)
        result["value"] = from_union([from_int, from_none], self.value)
        result["compareAmountAgentsHigh"] = from_union([from_str, from_none], self.compare_amount_agents_high)
        result["thresholdAmountAgentsHigh"] = from_union([from_int, from_none], self.threshold_amount_agents_high)
        result["compareAmountAgentsLow"] = from_union([from_str, from_none], self.compare_amount_agents_low)
        result["thresholdAmountAgentsLow"] = from_union([from_int, from_none], self.threshold_amount_agents_low)
        return result


@dataclass
class AgentRulePrecondition:
    identifier: Condition
    options: FluffyOptions

    @staticmethod
    def from_dict(obj: Any) -> 'AgentRulePrecondition':
        assert isinstance(obj, dict)
        identifier = Condition(obj.get("identifier"))
        options = FluffyOptions.from_dict(obj.get("options"))
        return AgentRulePrecondition(identifier, options)

    def to_dict(self) -> dict:
        result: dict = {}
        result["identifier"] = to_enum(Condition, self.identifier)
        result["options"] = to_class(FluffyOptions, self.options)
        return result


@dataclass
class AgentRule:
    name: str
    description: Optional[str]
    type: str
    preconditions: List[AgentRulePrecondition]
    postconditions: List[RulePoscondition]

    @staticmethod
    def from_dict(obj: Any) -> 'AgentRule':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        description = from_union([from_str, from_none], obj.get("description"))
        type = from_str(obj.get("type"))
        preconditions = from_list(AgentRulePrecondition.from_dict, obj.get("preconditions"))
        postconditions = from_list(RulePoscondition.from_dict, obj.get("postconditions"))
        return AgentRule(name, description, type, preconditions, postconditions)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["description"] = from_union([from_str, from_none], self.description)
        result["type"] = from_str(self.type)
        result["preconditions"] = from_list(lambda x: to_class(AgentRulePrecondition, x), self.preconditions)
        result["postconditions"] = from_list(lambda x: to_class(RulePoscondition, x), self.postconditions)
        return result


@dataclass
class AgentType:
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'AgentType':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        return AgentType(name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        return result


@dataclass
class LocatedAt:
    x: int
    y: int

    @staticmethod
    def from_dict(obj: Any) -> 'LocatedAt':
        assert isinstance(obj, dict)
        x = from_int(obj.get("x"))
        y = from_int(obj.get("y"))
        return LocatedAt(x, y)

    def to_dict(self) -> dict:
        result: dict = {}
        result["x"] = from_int(self.x)
        result["y"] = from_int(self.y)
        return result


@dataclass
class Agent:
    name: int
    type: str
    located_at: LocatedAt
    properties: List[Property]

    @staticmethod
    def from_dict(obj: Any) -> 'Agent':
        assert isinstance(obj, dict)
        name = int(from_str(obj.get("name")))
        type = from_str(obj.get("type"))
        located_at = LocatedAt.from_dict(obj.get("locatedAt"))
        properties = from_list(Property.from_dict, obj.get("properties"))
        return Agent(name, type, located_at, properties)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(str(self.name))
        result["type"] = from_str(self.type)
        result["locatedAt"] = to_class(LocatedAt, self.located_at)
        result["properties"] = from_list(lambda x: to_class(Property, x), self.properties)
        return result


@dataclass
class Coordinate:
    x: int
    y: int
    properties: List[Property]

    @staticmethod
    def from_dict(obj: Any) -> 'Coordinate':
        assert isinstance(obj, dict)
        x = from_int(obj.get("x"))
        y = from_int(obj.get("y"))
        properties = from_list(Property.from_dict, obj.get("properties"))
        return Coordinate(x, y, properties)

    def to_dict(self) -> dict:
        result: dict = {}
        result["x"] = from_int(self.x)
        result["y"] = from_int(self.y)
        result["properties"] = from_list(lambda x: to_class(Property, x), self.properties)
        return result


@dataclass
class Territory:
    width: int
    height: int
    default_coordinate: Optional[Coordinate]
    coordinates: Optional[List[Coordinate]]

    @staticmethod
    def from_dict(obj: Any) -> 'Territory':
        assert isinstance(obj, dict)
        width = from_int(obj.get("width"))
        height = from_int(obj.get("height"))
        default_coordinate = from_union([Coordinate.from_dict, from_none], obj.get("defaultCoordinate"))
        coordinates = from_union([lambda x: from_list(Coordinate.from_dict, x), from_none], obj.get("coordinates"))
        return Territory(width, height, default_coordinate, coordinates)

    def to_dict(self) -> dict:
        result: dict = {}
        result["width"] = from_int(self.width)
        result["height"] = from_int(self.height)
        if self.default_coordinate is not None:
            result["defaultCoordinate"] = from_union([lambda x: to_class(Coordinate, x), from_none], self.default_coordinate)
        if self.coordinates is not None:
            result["coordinates"] = from_union([lambda x: from_list(lambda x: to_class(Coordinate, x), x), from_none], self.coordinates)
        return result


@dataclass
class TerritoryRulePrecondition:
    identifier: Condition
    options: FluffyOptions

    @staticmethod
    def from_dict(obj: Any) -> 'TerritoryRulePrecondition':
        assert isinstance(obj, dict)
        identifier = Condition(obj.get("identifier"))
        options = FluffyOptions.from_dict(obj.get("options"))
        return TerritoryRulePrecondition(identifier, options)

    def to_dict(self) -> dict:
        result: dict = {}
        result["identifier"] = to_enum(Condition, self.identifier)
        result["options"] = to_class(FluffyOptions, self.options)
        return result


@dataclass
class TerritoryRule:
    name: str
    description: Optional[str]
    preconditions: List[TerritoryRulePrecondition]
    postconditions: List[RulePoscondition]

    @staticmethod
    def from_dict(obj: Any) -> 'TerritoryRule':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        description = from_union([from_str, from_none], obj.get("description"))
        preconditions = from_list(TerritoryRulePrecondition.from_dict, obj.get("preconditions"))
        postconditions = from_list(RulePoscondition.from_dict, obj.get("postconditions"))
        return TerritoryRule(name, description, preconditions, postconditions)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["description"] = from_union([from_str, from_none], self.description)
        result["preconditions"] = from_list(lambda x: to_class(TerritoryRulePrecondition, x), self.preconditions)
        result["postconditions"] = from_list(lambda x: to_class(RulePoscondition, x), self.postconditions)
        return result


@dataclass
class SimulationClass:
    name: str
    steps: int
    territory: Territory
    agents: List[Agent]
    agent_type: List[AgentType]
    agent_properties: List[AgentProperty]
    coordinate_properties: List[AgentType]
    agent_rules: List[AgentRule]
    territory_rules: List[TerritoryRule]

    @staticmethod
    def from_dict(obj: Any) -> 'SimulationClass':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        steps = from_int(obj.get("steps"))
        territory = Territory.from_dict(obj.get("territory"))
        agents = from_list(Agent.from_dict, obj.get("agents"))
        agent_type = from_list(AgentType.from_dict, obj.get("AgentType"))
        agent_properties = from_list(AgentProperty.from_dict, obj.get("AgentProperties"))
        coordinate_properties = from_list(AgentType.from_dict, obj.get("CoordinateProperties"))
        agent_rules = from_list(AgentRule.from_dict, obj.get("AgentRules"))
        territory_rules = from_list(TerritoryRule.from_dict, obj.get("TerritoryRules"))
        return SimulationClass(name, steps, territory, agents, agent_type, agent_properties, coordinate_properties, agent_rules, territory_rules)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["steps"] = from_int(self.steps)
        result["territory"] = to_class(Territory, self.territory)
        result["agents"] = from_list(lambda x: to_class(Agent, x), self.agents)
        result["AgentType"] = from_list(lambda x: to_class(AgentType, x), self.agent_type)
        result["AgentProperties"] = from_list(lambda x: to_class(AgentProperty, x), self.agent_properties)
        result["CoordinateProperties"] = from_list(lambda x: to_class(AgentType, x), self.coordinate_properties)
        result["AgentRules"] = from_list(lambda x: to_class(AgentRule, x), self.agent_rules)
        result["TerritoryRules"] = from_list(lambda x: to_class(TerritoryRule, x), self.territory_rules)
        return result


@dataclass
class Simulation:
    simulation: SimulationClass

    @staticmethod
    def from_dict(obj: Any) -> 'Simulation':
        assert isinstance(obj, dict)
        simulation = SimulationClass.from_dict(obj.get("simulation"))
        return Simulation(simulation)

    def to_dict(self) -> dict:
        result: dict = {}
        result["simulation"] = to_class(SimulationClass, self.simulation)
        return result


def simulation_from_dict(s: Any) -> Simulation:
    """
    Partially generated with https://app.quicktype.io/
    """
    return Simulation.from_dict(s)
