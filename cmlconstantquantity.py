from stackhelpers import get_next_parentheses_unit
from cmlclasses import Unit
from cmlunit import parse_dimension_from_quantity_expression
from cmlparser import CMLParser
from typing import List, Tuple
from cmltokens import TokenType


def parse_constant_quantity(parser: CMLParser, stack: List[Tuple[TokenType, any]]):
    """[summary]

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
    assert new_unit.name not in parser.scope.units,\
           f"Dimension {new_unit.name} already exists"
    tok = stack.pop()
    if tok[0] == TokenType.DIMENSION_ATTRIBUTE:
        tok = stack.pop()
        assert tok[1] in parser.scope.dimensions,\
               "Dimension supplied does not exist"
        new_unit.dimension = parser.scope.dimensions[tok[1]]
        new_unit.base_unit = True
        parser.scope.units[new_unit.name] = new_unit
    else:
        assert tok[0] == TokenType.ASSIGNMENT_ATTRIBUTE,\
               "Invalid unit expression"
        unit_expression = get_next_parentheses_unit(stack)
        new_unit.quantity_expression = unit_expression
        new_unit.dimension = parse_dimension_from_quantity_expression(
                                parser, unit_expression)

        assert new_unit.dimension is not None,\
               f"Invalid quantity expression for {new_unit.name}"

        # Add the dimension to the parser.
        parser.scope.units[new_unit.name] = new_unit

    return

def parse_quantity_expression_value(parser, stack):

    working_stack = []
    paren_count = 0

    while len(stack) > 0:
        tok = stack.pop()

        if tok[0] == TokenType.LEFT_PARENTHESES:
            paren_count += 1
            working_stack.append(tok)
        elif tok[0] == TokenType.RIGHT_PARENTHESES:


