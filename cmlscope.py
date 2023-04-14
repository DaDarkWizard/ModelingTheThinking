"""
All scope related functions.
"""

from typing import List, Tuple, Dict
from cmltokens import TokenType
from cmlclasses import Unit, Dimension, Relation, ModelFragment,\
        Scenario, QuantityFunction, CMLObject
from lispclasses import Macro


class CMLScope:
    """
    Storage class for objects and types within a certain scope.
    """

    def __init__(self):
        self.parent = None
        self.stack: List[Tuple[TokenType, any]] = []
        self.__objconsts: Dict[str, any] = {}

    def objconsts(self):
        """
        Returns the dictionary of all object constants in scope.
        """
        results = {}
        if isinstance(self.parent, CMLScope):
            results = self.parent.objconsts()
        for k, v in self.__objconsts.items():
            results[k] = v
        return results

    def units(self):
        """
        Returns the dictionary of all units in scope.
        """
        return dict((k, v) for k, v in self.objconsts().items()
                    if isinstance(v, Unit))

    def add_unit(self, unit: Unit):
        """
        Adds a unit to the scope.
        """
        assert unit.name not in self.objconsts(),\
               "objconst already exists for unit definition."
        self.__objconsts[unit.name] = unit

    def get_unit(self, unit_name: str):
        """
        Gets a unit from the scope.
        """
        assert unit_name in self.objconsts(),\
               "Unit name does not exists"
        assert isinstance(self.objconsts()[unit_name], Unit),\
               "Objconst is not unit"
        return self.objconsts()[unit_name]

    def dimensions(self):
        """
        Returns a dictionary of all dimensions in scope.
        """
        return dict((k, v) for k, v in self.objconsts().items()
                    if isinstance(v, Dimension))

    def add_dimension(self, dimension: Dimension):
        """
        Adds a dimension to the scope.
        """
        assert dimension.name not in self.objconsts(),\
               "objconst already exists for dimension definition."
        self.__objconsts[dimension.name] = dimension

    def get_dimension(self, dimension_name: str):
        """
        Gets a dimension from the scope.
        """
        assert dimension_name in self.objconsts(),\
               "Dimension name does not exists"
        assert isinstance(self.objconsts()[dimension_name], Dimension),\
               "Objconst is not diemension"
        return self.objconsts()[dimension_name]

    def relations(self):
        """
        Returns a dictionary of all relations in scope.
        """
        return dict((k, v) for k, v in self.objconsts().items()
                    if isinstance(v, Relation))

    def add_relation(self, relation: Relation):
        """
        Adds a relation to the scope.
        """
        assert relation.name not in self.objconsts(),\
               "objconst already exists for relation definition."
        self.__objconsts[relation.name] = relation

    def get_relation(self, relation_name: str):
        """
        Gets a relation from the scope.
        """
        assert relation_name in self.objconsts(),\
               "Relation name does not exists"
        assert isinstance(self.objconsts()[relation_name], Relation),\
               "Objconst is not diemension"
        return self.objconsts()[relation_name]

    def modelfragments(self):
        """
        Returns a dictionary of all modelfragments in scope.
        """
        return dict((k, v) for k, v in self.objconsts().items()
                    if isinstance(v, ModelFragment))

    def add_modelfragment(self, modelfragment: ModelFragment):
        """
        Adds a modelfragment to the scope.
        """
        assert modelfragment.name not in self.objconsts(),\
               "objconst already exists for modelfragment definition."
        self.__objconsts[modelfragment.name] = modelfragment

    def get_modelfragment(self, modelfragment_name: str):
        """
        Gets a modelfragment from the scope.
        """
        assert modelfragment_name in self.objconsts(),\
               "ModelFragment name does not exists"
        assert isinstance(self.objconsts()[modelfragment_name],
                          ModelFragment),\
               "Objconst is not diemension"
        return self.objconsts()[modelfragment_name]

    def scenarios(self):
        """
        Returns a dictionary of all scenarios in scope.
        """
        return dict((k, v) for k, v in self.objconsts().items()
                    if isinstance(v, Scenario))

    def add_scenario(self, scenario: Scenario):
        """
        Adds a scenario to the scope.
        """
        assert scenario.name not in self.objconsts(),\
               "objconst already exists for scenario definition."
        self.__objconsts[scenario.name] = scenario

    def get_scenario(self, scenario_name: str):
        """
        Gets a scenario from the scope.
        """
        assert scenario_name in self.objconsts(),\
               "Scenario name does not exists"
        assert isinstance(self.objconsts()[scenario_name],
                          Scenario),\
               "Objconst is not diemension"
        return self.objconsts()[scenario_name]

    def quantityfunctions(self):
        """
        Returns a dictionary of all quantityfunctions in scope.
        """
        return dict((k, v) for k, v in self.objconsts().items()
                    if isinstance(v, QuantityFunction))

    def add_quantityfunction(self, quantityfunction: QuantityFunction):
        """
        Adds a quantityfunction to the scope.
        """
        assert quantityfunction.name not in self.objconsts(),\
               "objconst already exists for quantityfunction definition."
        self.__objconsts[quantityfunction.name] = quantityfunction

    def get_quantityfunction(self, quantityfunction_name: str):
        """
        Gets a quantityfunction from the scope.
        """
        assert quantityfunction_name in self.objconsts(),\
               "QuantityFunction name does not exists"
        assert isinstance(self.objconsts()[quantityfunction_name],
                          QuantityFunction),\
               "Objconst is not diemension"
        return self.objconsts()[quantityfunction_name]

    def cmlobjects(self):
        """
        Returns a dictionary of all cmlobjects in scope.
        """
        return dict((k, v) for k, v in self.objconsts().items()
                    if isinstance(v, CMLObject))

    def add_cmlobject(self, cmlobject: CMLObject):
        """
        Adds a cmlobject to the scope.
        """
        assert cmlobject.name not in self.objconsts(),\
               "objconst already exists for quantityfunction definition."
        self.__objconsts[cmlobject.name] = cmlobject

    def get_cmlobject(self, cmlobject_name: str):
        """
        Gets a cmlobject from the scope.
        """
        assert cmlobject_name in self.objconsts(),\
               "CMLObject name does not exists"
        assert isinstance(self.objconsts()[cmlobject_name],
                          CMLObject),\
               "Objconst is not cmlobject"
        return self.objconsts()[cmlobject_name]

    def lispobjects(self):
        """
        Returns a dictionary of all lispobjects in scope.
        """
        return dict((k, v) for k, v in self.objconsts().items()
                    if isinstance(v, Tuple))

    def set_lispobject(self, name, lispobject: Tuple):
        """
        Adds a lispobject to the scope.
        """
        self.__objconsts[name] = lispobject

    def get_lispobject(self, name: str):
        """
        Gets a lispobject from the scope.
        """
        assert name in self.objconsts(),\
               f"Object {name} does not exists"
        assert isinstance(self.objconsts()[name],
                          Tuple),\
               f"Object {name} is not a lisp object"
        return self.objconsts()[name]
