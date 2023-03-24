"""
All scope related functions.
"""

from typing import List, Tuple, Dict
from cmltokens import TokenType
from cmlclasses import Unit, Dimension, Relation


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
               "Unit name does not exists"
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
               "Unit name does not exists"
        assert isinstance(self.objconsts()[relation_name], Relation),\
               "Objconst is not diemension"
        return self.objconsts()[relation_name]
