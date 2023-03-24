"""
Handles all functions for parsing a CML unit.

Daniel Masker
23-03-2023

"""
from typing import List, Tuple
from stackhelpers import get_next_parentheses_unit
from cmlclasses import Unit, ModelValue
from cmlparser import CMLParser
from cmltokens import TokenType
from cmlmath import parse_math_expression


def parse_unit(parser: CMLParser, stack: List[Tuple[TokenType, any]]):
    """
    [summary]

        Parses a stack containing a unit description.

        The stack will come in without the first parentheses or defUnit.

        ### Parameters
        1. parser: CMLParser
           - The cml parser we are using.
        2. stack: List[Tuple[TokenType, any]]
           - The stack to parse the unit from.
    """

    tok = stack.pop()
    assert tok[0] == TokenType.IDENTIFIER, "Unit given without a name"
    new_unit = Unit(tok[1])
    assert new_unit.name not in parser.scope.units(),\
           f"Dimension {new_unit.name} already exists"
    tok = stack.pop()
    if tok[0] == TokenType.DIMENSION_ATTRIBUTE:
        tok = stack.pop()
        assert tok[1] in parser.scope.dimensions(),\
               "Dimension supplied does not exist"
        new_unit_value = ModelValue()
        new_unit_value.dimension = parser.scope.get_dimension(tok[1])\
                                         .dimension.copy()
        new_unit_value.quantity = 1
        new_unit.value = new_unit_value

        new_unit.base_unit = True
        parser.scope.add_unit(new_unit)
    else:
        assert tok[0] == TokenType.ASSIGNMENT_ATTRIBUTE,\
               "Invalid unit expression"
        unit_expression = get_next_parentheses_unit(stack)
        unit_expression.reverse()
        unit_value = parse_math_expression(parser, unit_expression)
        assert unit_value[0] == TokenType.MODEL_VALUE,\
               "Result of unit expression should be a value."
        new_unit.value = unit_value[1]
        assert new_unit.value.dimension is not None,\
               f"Invalid quantity expression for {new_unit.name}"

        # Add the dimension to the parser.
        parser.scope.add_unit(new_unit)


# def parse_dimension_from_quantity_expression(parser, stack):
#     for tok in stack:
#         if tok[0] == TokenType.IDENTIFIER and\
#            tok[1] in parser.scope.dimensions():
#             return parser.scope.get_dimension(tok[1])
#         elif tok[0] == TokenType.IDENTIFIER and\
#                 tok[1] in parser.scope.units():
#             return parser.scope.get_unit(tok[1]).dimension
#     return None
