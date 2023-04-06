"""
Handles all functions for modelfragment in CML
"""
from typing import List, Tuple
from cmltokens import TokenType
from cmlparser import CMLParser
from cmlclasses import Scenario
from stackhelpers import get_next_parentheses_unit


def parse_scenario(parser: CMLParser,
                   stack: List[Tuple[TokenType, any]]):
    [Summary]

    Parsers a modelfragment object from a CML definition.
    """
    """
    tok = stack.pop()
    assert tok[0] == TokenType.IDENTIFIER,\
           "ModelFragment given without a valid name."

    new_model = Scenario(tok[1])

    while len(stack) > 1:

        if stack[-1][0] == TokenType.IDENTIFIER and\
           stack[-1][1] == ":individuals":
            stack.pop()
            new_model.conditions = get_next_parentheses_unit(stack)

        elif stack[-1][0] == TokenType.IDENTIFIER and\
                stack[-1][1] == ":initially":
            stack.pop()
            new_model.quantities = get_next_parentheses_unit(stack)

        elif stack[-1][0] == TokenType.IDENTIFIER and\
                stack[-1][1] == ":throughout":
            stack.pop()
            new_model.attributes = get_next_parentheses_unit(stack)

        elif stack[-1][0] == TokenType.IDENTIFIER and\
                stack[-1][1] == ":boundary":
            new_model.consequences = get_next_parentheses_unit(stack)

        elif stack[-1][0] == TokenType.IDENTIFIER and\
                stack[-1][1] == ":documentation":
            new_model.consequences = get_next_parentheses_unit(stack)

        elif stack[-1][0] == TokenType.IDENTIFIER and\
                stack[-1][1] == ":substitutions":
            new_model.consequences = get_next_parentheses_unit(stack)

        else:
            raise Exception("Unknown element in scenario definition.")

    parser.scope.add_scenario(new_model)
