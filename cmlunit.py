from stackhelpers import get_next_parentheses_unit
from cmlclasses import Unit
from cmlparser import CMLParser
from typing import List, Tuple
from cmltokens import TokenType


def parse_unit(parser: CMLParser, stack: List[Tuple[TokenType, any]]):
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
    assert new_unit.name not in parser.scope.units(),\
           f"Dimension {new_unit.name} already exists"
    tok = stack.pop()
    if tok[0] == TokenType.DIMENSION_ATTRIBUTE:
        tok = stack.pop()
        assert tok[1] in parser.scope.dimensions(),\
               "Dimension supplied does not exist"
        new_unit.dimension = parser.scope.get_dimension(tok[1])
        new_unit.base_unit = True
        parser.scope.add_unit(new_unit)
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
        parser.scope.add_unit(new_unit)

    return


def parse_dimension_from_quantity_expression(parser, stack):
    for tok in stack:
        if tok[0] == TokenType.IDENTIFIER and\
           tok[1] in parser.scope.dimensions():
            return parser.scope.dimensions[tok[1]]
        elif tok[0] == TokenType.IDENTIFIER and\
                tok[1] in parser.scope.units():
            return parser.scope.get_unit(tok[1]).dimension

    return None

# def parse_unit_expression(parser, stack):
#
#     working_stack = []
#     paren_count = 0
#
#     def identifier_to_dimension(id):
#         assert id[0] == TokenType.IDENTIFIER, "Invalid dimension given"
#         assert id[1] in parser.scope.dimensions,\
#                "Undefined dimension in dimension definision"
#         # dim_value = dict()
#         # dim_value[id[1]] = 1
#         return (TokenType.DIMENSION_VALUE,
#                 parser.scope.dimensions[id[1]].dimension.copy())
#
#     while len(stack) > 0:
#         tok = stack.pop()
#         if tok[0] == TokenType.LEFT_PARENTHESES:
#             paren_count += 1
#             working_stack.append(tok)
#         elif tok[0] == TokenType.RIGHT_PARENTHESES:
#             paren_count -= 1
#
#             arg2 = working_stack.pop()
#             if arg2[0] == TokenType.IDENTIFIER:
#                 arg2 = identifier_to_dimension(arg2)
#             arg1 = working_stack.pop()
#             if arg1[0] == TokenType.IDENTIFIER:
#                 arg1 = identifier_to_dimension(arg1)
#             elif arg1[0] == TokenType.LEFT_PARENTHESES:
#                 working_stack.append(arg2)
#                 continue
#
#             func = working_stack.pop()
#             if func[0] == TokenType.STAR:
#                 for name, value in arg2[1].items():
#                     if name in arg1[1]:
#                         arg1[1][name] += value
#                     else:
#                         arg1[1][name] = value
#             elif func[0] == TokenType.DIVIDE:
#                 for name, value in arg2[1].items():
#                     if name in arg1[1]:
#                         arg1[1][name] -= value
#                     else:
#                         arg1[1][name] = -1 * value
#             elif func[0] == TokenType.EXPT:
#                 for name, value in arg1[1].items():
#                     arg1[1][name] = value * arg2[1]
#             else:
#                 raise Exception("Invalid dimension expression")
#
#             working_stack.append(arg1)
#
#             if paren_count == 0:
#                 return working_stack.pop()
#         else:
#             working_stack.append(tok)
#
#     return working_stack.pop()
