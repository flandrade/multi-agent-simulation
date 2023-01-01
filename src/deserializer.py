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


class Name(Enum):
    FOOD = "food"
    IS_ALIVE = "is-alive"
    LOAD = "load"


class Condition(Enum):
    CHECK_PRESENCE = "check-presence"
    COMPARE_PROPERTY = "compare-property"


class Compare(Enum):
    EQUAL = "equal"
    GREATER_THAN = "greater-than"
    LESS_THAN = "less-than"


@dataclass
class AgentProperty:
    name: Name
    represent_liveness: bool

    @staticmethod
    def from_dict(obj: Any) -> 'AgentProperty':
        assert isinstance(obj, dict)
        name = Name(obj.get("name"))
        represent_liveness = from_bool(obj.get("representLiveness"))
        return AgentProperty(name, represent_liveness)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = to_enum(Name, self.name)
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
    probability_of_changing: Optional[int] = None
    property_agent: Optional[Name] = None
    property_territory: Optional[str] = None
    type: Optional[str] = None
    value: Optional[int] = None
    steps: Optional[int] = None
    direction: Optional[str] = None
    affected: Optional[str] = None
    compare: Optional[str] = None
    amount: Optional[int] = None
    probability_of_adding: Optional[int] = None
    properties: Optional[List[Property]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PurpleOptions':
        assert isinstance(obj, dict)
        probability_of_changing = from_union([from_int, from_none], obj.get("probabilityOfChanging"))
        property_agent = from_union([from_none, Name], obj.get("propertyAgent"))
        property_territory = from_union([from_none, from_str], obj.get("propertyTerritory"))
        type = from_union([from_str, from_none], obj.get("type"))
        value = from_union([from_int, from_none], obj.get("value"))
        steps = from_union([from_int, from_none], obj.get("steps"))
        direction = from_union([from_str, from_none], obj.get("direction"))
        affected = from_union([from_str, from_none], obj.get("affected"))
        compare = from_union([from_str, from_none], obj.get("compare"))
        amount = from_union([from_int, from_none], obj.get("amount"))
        probability_of_adding = from_union([from_int, from_none], obj.get("probabilityOfAdding"))
        properties = from_union([lambda x: from_list(Property.from_dict, x), from_none], obj.get("properties"))
        return PurpleOptions(probability_of_changing, property_agent, property_territory, type, value, steps, direction, affected, compare, amount, probability_of_adding, properties)

    def to_dict(self) -> dict:
        result: dict = {}
        result["probabilityOfChanging"] = from_union([from_int, from_none], self.probability_of_changing)
        result["propertyAgent"] = from_union([from_none, lambda x: to_enum(Name, x)], self.property_agent)
        result["propertyTerritory"] = from_union([from_none, from_str], self.property_territory)
        result["type"] = from_union([from_str, from_none], self.type)
        result["value"] = from_union([from_int, from_none], self.value)
        result["steps"] = from_union([from_int, from_none], self.steps)
        result["direction"] = from_union([from_str, from_none], self.direction)
        result["affected"] = from_union([from_str, from_none], self.affected)
        result["compare"] = from_union([from_str, from_none], self.compare)
        result["amount"] = from_union([from_int, from_none], self.amount)
        result["probabilityOfAdding"] = from_union([from_int, from_none], self.probability_of_adding)
        result["properties"] = from_union([lambda x: from_list(lambda x: to_class(Property, x), x), from_none], self.properties)
        return result


@dataclass
class AgentRulePoscondition:
    action: str
    options: PurpleOptions

    @staticmethod
    def from_dict(obj: Any) -> 'AgentRulePoscondition':
        assert isinstance(obj, dict)
        action = from_str(obj.get("action"))
        options = PurpleOptions.from_dict(obj.get("options"))
        return AgentRulePoscondition(action, options)

    def to_dict(self) -> dict:
        result: dict = {}
        result["action"] = from_str(self.action)
        result["options"] = to_class(PurpleOptions, self.options)
        return result


@dataclass
class FluffyOptions:
    property_agent: Optional[Name] = None
    property_territory: Optional[Name] = None
    compare: Optional[Compare] = None
    threshold: Optional[int] = None
    type: Optional[str] = None
    value: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'FluffyOptions':
        assert isinstance(obj, dict)
        property_agent = from_union([from_none, Name], obj.get("propertyAgent"))
        property_territory = from_union([from_none, Name], obj.get("propertyTerritory"))
        compare = from_union([Compare, from_none], obj.get("compare"))
        threshold = from_union([from_int, from_none], obj.get("threshold"))
        type = from_union([from_str, from_none], obj.get("type"))
        value = from_union([from_int, from_none], obj.get("value"))
        return FluffyOptions(property_agent, property_territory, compare, threshold, type, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["propertyAgent"] = from_union([from_none, lambda x: to_enum(Name, x)], self.property_agent)
        result["propertyTerritory"] = from_union([from_none, lambda x: to_enum(Name, x)], self.property_territory)
        result["compare"] = from_union([lambda x: to_enum(Compare, x), from_none], self.compare)
        result["threshold"] = from_union([from_int, from_none], self.threshold)
        result["type"] = from_union([from_str, from_none], self.type)
        result["value"] = from_union([from_int, from_none], self.value)
        return result


@dataclass
class AgentRulePrecondition:
    condition: Condition
    options: FluffyOptions

    @staticmethod
    def from_dict(obj: Any) -> 'AgentRulePrecondition':
        assert isinstance(obj, dict)
        condition = Condition(obj.get("condition"))
        options = FluffyOptions.from_dict(obj.get("options"))
        return AgentRulePrecondition(condition, options)

    def to_dict(self) -> dict:
        result: dict = {}
        result["condition"] = to_enum(Condition, self.condition)
        result["options"] = to_class(FluffyOptions, self.options)
        return result


@dataclass
class AgentRule:
    name: str
    description: str
    type: str
    preconditions: List[AgentRulePrecondition]
    posconditions: List[AgentRulePoscondition]

    @staticmethod
    def from_dict(obj: Any) -> 'AgentRule':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        description = from_str(obj.get("description"))
        type = from_str(obj.get("type"))
        preconditions = from_list(AgentRulePrecondition.from_dict, obj.get("preconditions"))
        posconditions = from_list(AgentRulePoscondition.from_dict, obj.get("posconditions"))
        return AgentRule(name, description, type, preconditions, posconditions)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["description"] = from_str(self.description)
        result["type"] = from_str(self.type)
        result["preconditions"] = from_list(lambda x: to_class(AgentRulePrecondition, x), self.preconditions)
        result["posconditions"] = from_list(lambda x: to_class(AgentRulePoscondition, x), self.posconditions)
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
class Configuration:
    x: int
    y: int
    properties: List[Property]

    @staticmethod
    def from_dict(obj: Any) -> 'Configuration':
        assert isinstance(obj, dict)
        x = from_int(obj.get("x"))
        y = from_int(obj.get("y"))
        properties = from_list(Property.from_dict, obj.get("properties"))
        return Configuration(x, y, properties)

    def to_dict(self) -> dict:
        result: dict = {}
        result["x"] = from_int(self.x)
        result["y"] = from_int(self.y)
        result["properties"] = from_list(lambda x: to_class(Property, x), self.properties)
        return result


@dataclass
class Coordinates:
    default_properties: List[Property]
    configuration: List[Configuration]

    @staticmethod
    def from_dict(obj: Any) -> 'Coordinates':
        assert isinstance(obj, dict)
        default_properties = from_list(Property.from_dict, obj.get("defaultProperties"))
        configuration = from_list(Configuration.from_dict, obj.get("configuration"))
        return Coordinates(default_properties, configuration)

    def to_dict(self) -> dict:
        result: dict = {}
        result["defaultProperties"] = from_list(lambda x: to_class(Property, x), self.default_properties)
        result["configuration"] = from_list(lambda x: to_class(Configuration, x), self.configuration)
        return result


@dataclass
class Territory:
    width: int
    height: int
    coordinates: Coordinates

    @staticmethod
    def from_dict(obj: Any) -> 'Territory':
        assert isinstance(obj, dict)
        width = from_int(obj.get("width"))
        height = from_int(obj.get("height"))
        coordinates = Coordinates.from_dict(obj.get("coordinates"))
        return Territory(width, height, coordinates)

    def to_dict(self) -> dict:
        result: dict = {}
        result["width"] = from_int(self.width)
        result["height"] = from_int(self.height)
        result["coordinates"] = to_class(Coordinates, self.coordinates)
        return result


@dataclass
class TentacledOptions:
    probability_of_changing: float
    property_agent: None
    property_territory: str
    type: str
    value: int

    @staticmethod
    def from_dict(obj: Any) -> 'TentacledOptions':
        assert isinstance(obj, dict)
        probability_of_changing = from_float(obj.get("probabilityOfChanging"))
        property_agent = from_none(obj.get("propertyAgent"))
        property_territory = from_str(obj.get("propertyTerritory"))
        type = from_str(obj.get("type"))
        value = from_int(obj.get("value"))
        return TentacledOptions(probability_of_changing, property_agent, property_territory, type, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["probabilityOfChanging"] = to_float(self.probability_of_changing)
        result["propertyAgent"] = from_none(self.property_agent)
        result["propertyTerritory"] = from_str(self.property_territory)
        result["type"] = from_str(self.type)
        result["value"] = from_int(self.value)
        return result


@dataclass
class TerritoryRulePoscondition:
    action: str
    options: TentacledOptions

    @staticmethod
    def from_dict(obj: Any) -> 'TerritoryRulePoscondition':
        assert isinstance(obj, dict)
        action = from_str(obj.get("action"))
        options = TentacledOptions.from_dict(obj.get("options"))
        return TerritoryRulePoscondition(action, options)

    def to_dict(self) -> dict:
        result: dict = {}
        result["action"] = from_str(self.action)
        result["options"] = to_class(TentacledOptions, self.options)
        return result


@dataclass
class StickyOptions:
    property_agent: None
    property_territory: str
    compare: Compare
    threshold: int

    @staticmethod
    def from_dict(obj: Any) -> 'StickyOptions':
        assert isinstance(obj, dict)
        property_agent = from_none(obj.get("propertyAgent"))
        property_territory = from_str(obj.get("propertyTerritory"))
        compare = Compare(obj.get("compare"))
        threshold = from_int(obj.get("threshold"))
        return StickyOptions(property_agent, property_territory, compare, threshold)

    def to_dict(self) -> dict:
        result: dict = {}
        result["propertyAgent"] = from_none(self.property_agent)
        result["propertyTerritory"] = from_str(self.property_territory)
        result["compare"] = to_enum(Compare, self.compare)
        result["threshold"] = from_int(self.threshold)
        return result


@dataclass
class TerritoryRulePrecondition:
    condition: Condition
    options: StickyOptions

    @staticmethod
    def from_dict(obj: Any) -> 'TerritoryRulePrecondition':
        assert isinstance(obj, dict)
        condition = Condition(obj.get("condition"))
        options = StickyOptions.from_dict(obj.get("options"))
        return TerritoryRulePrecondition(condition, options)

    def to_dict(self) -> dict:
        result: dict = {}
        result["condition"] = to_enum(Condition, self.condition)
        result["options"] = to_class(StickyOptions, self.options)
        return result


@dataclass
class TerritoryRule:
    name: str
    description: str
    preconditions: List[TerritoryRulePrecondition]
    posconditions: List[TerritoryRulePoscondition]

    @staticmethod
    def from_dict(obj: Any) -> 'TerritoryRule':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        description = from_str(obj.get("description"))
        preconditions = from_list(TerritoryRulePrecondition.from_dict, obj.get("preconditions"))
        posconditions = from_list(TerritoryRulePoscondition.from_dict, obj.get("posconditions"))
        return TerritoryRule(name, description, preconditions, posconditions)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["description"] = from_str(self.description)
        result["preconditions"] = from_list(lambda x: to_class(TerritoryRulePrecondition, x), self.preconditions)
        result["posconditions"] = from_list(lambda x: to_class(TerritoryRulePoscondition, x), self.posconditions)
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
    return Simulation.from_dict(s)
