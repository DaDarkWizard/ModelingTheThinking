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
        self.dimension: Dict[str, int] = dimension
    
    def to_string(self):
        x = f"(defDimension {self.name} :documentation \"{self.documentation}\" "
        if len(self.dimension) == 1 and self.dimension[list(self.dimension.keys())[0]] == 1:
            x += ")"
            return x
        else:
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