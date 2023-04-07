from typing import List, Dict, Tuple
from cmltokens import TokenType


class Relation:
    def __init__(self, name: str, args: List[str], documentation: str = "",
                 implication: List[Tuple[str, any]] = [],
                 iff: List[Tuple[str, any]] = [], function: bool = True,
                 time_dependent: bool = False):
        self.name = name
        self.args = args
        self.documentation = documentation
        self.implication = implication.copy()
        self.iff = iff.copy()
        self.function = function
        self.time_dependent = time_dependent
        self.addons = {}


class QuantityFunction:
    def __init__(self, name: str, args: List[str]):
        self.name = name
        self.args = args
        self.implication = None
        self.documentation = ""
        self.sentence = None
        self.dimension = None
        self.piecewise_continuous = None
        self.step_quantity = None
        self.count_quantity = None
        self.non_numeric = None
        self.addons = {}



class ModelFragment:
    def __init__(self, name : str):
        self.name = name
        self.documentation = None
        self.implication: List[Tuple[TokenType, any]] = []
        self.sub_class_of = None
        self.participants = None
        self.conditions = None
        self.quantities = None
        self.attributes = None
        self.consequences = None
        self.addons = {}
        self.substitutions = None

    def to_string(self):
        return f"({self.name})"

class Entity:
    def __init__(self, name: str, documentation: str = "", sub_class_of = object, 
                 quantities: List[Tuple[int, str]] = [], attributes: List[str] = [], consequences: str = ""):
        self.name = name
        self.documentation = documentation
        self.sub_class_of = sub_class_of
        self.quantities = quantities
        self.attributes = attributes
        self.consequences = consequences


class Dimension:
    def __init__(self, name: str, documentation: str = "", dimension=dict()):
        self.name = name
        self.documentation = documentation
        self.dimension: Dict[str, int] = dimension.copy()
        self.addons = {}

    def to_string(self):
        x = f"(defDimension {self.name}" +\
             " :documentation \"{self.documentation}\" "
        if len(self.dimension) == 1 and\
           self.dimension[list(self.dimension.keys())[0]] == 1:
            x += ")"
            return x
        else:
            x += " := "
            dim_items = list(self.dimension.items())
            paren_count = 0
            for i in range(len(dim_items)):
                if i == len(dim_items) - 1:
                    x += f" (expt {dim_items[i][0]} {dim_items[i][1]})"
                    while paren_count > 0:
                        x += ")"
                        paren_count -= 1
                else:
                    x += f" (* (expt {dim_items[i][0]} {dim_items[i][1]})"
                    paren_count += 1
            x += ")"

        return x


class ModelValue:
    def __init__(self):
        self.quantity = 0
        self.dimension = dict()

    def copy(self):
        result = ModelValue()
        result.quantity = self.quantity
        result.dimension = self.dimension.copy()
        return result

    def to_string(self):
        dim_items = list(self.dimension.items())
        paren_count = 0
        x = ""
        for i in range(len(dim_items)):
            if i == len(dim_items) - 1:
                x += f" (expt {dim_items[i][0]} {dim_items[i][1]})"
                while paren_count > 0:
                    x += ")"
                    paren_count -= 1
            else:
                x += f" (* (expt {dim_items[i][0]} {dim_items[i][1]})"
                paren_count += 1
        x += ")"
        return f"(* {self.quantity} {x})"


# constant quantities and units are the same thing
class Unit:
    def __init__(self, name: str, documentation: str = "",
                 value: ModelValue = ModelValue()):
        self.name = name
        self.documentation = documentation
        self.value = value.copy()
        self.addons = {}


class Scenario:

    def __init__(self, name: str, documentation: str = "",
                 individuals: dict[str, object] = {},
                 initially: str = "", throughout: str = ""):
        self.name = name
        self.documentation = documentation
        self.individuals = individuals.copy()
        self.initially = initially
        self.throughout = throughout
        self.addons = {}
