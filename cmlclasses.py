from typing import List, Dict, Tuple

class Relation:
    def __init__(self, name: str, args: List[str], documentation: str = "",
                 first_sentence = lambda args: False, secsentence = "", function = True, time_dependent = False ):
        self.name = name
        self.args = args
        self.documentation = documentation
        self.first_sentence = first_sentence
        self.secsentence = secsentence
        self.function = function
        self.time_dependent = time_dependent
        


class QuantityFunction:
    def __init__(self, name: str, args: List[str], documentation: str = "", sentence: str = "", 
                 dimension = lambda args: 0, piecewise: bool = True, step_quantity: bool = True,
                 count_quantity: bool = True, non_numeric: bool = True):
        self.name = name
        self.args = args
        self.documentation = documentation
        self.sentence = sentence
        self.dimension = dimension
        self.piecewise = piecewise
        self.step_quantity = step_quantity
        self.count_quality = count_quantity
        self.non_numeric = non_numeric



class ModelFragment:
    def __init__(self, name : str, documentation : str = "", sub_class_of = object,
                participants : List[Tuple[int, str]] = [], conditions : str = "", quantities : List[Tuple[int, str]] = [],
                attributes : List[str] = [], consequences : str = ""):
        self.name = name
        self.documentation = documentation
        self.sub_class_of = sub_class_of
        self.participants = participants
        self.conditions = conditions
        self.quantities = quantities
        self.attributes = attributes
        self.consequences = consequences
    

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
    def __init__(self, name : str, documentation : str = "", dimension = dict()): 
        self.name = name
        self.documentation = documentation
        self.dimension = dimension

class Unit:
    def __init__(self, name : str, documentation : str = "", quantity_expression = lambda args : 0,
                dimension = lambda args : 0):
        self.name = name
        self.documentation = documentation
        self.quantity_expression = quantity_expression
        self.dimension = dimension


class ConstantQuantity:
    def __init__(self, name : str, documentation : str = "", quantity_expression = lambda args : 0,
                dimension = lambda args : 0):
        self.name = name
        self.documentation = documentation
        self.quantity_expression = quantity_expression
        self.dimension = dimension

class Scenario:
    def __init__(self, name : str, documentation : str = "", individuals = dict[str, object],
                initially : str = "", throughout : str = ""):
        self.name = name
        self.documentation = documentation
        self.individuals = individuals
        self.initially = initially
        self.throughout = throughout