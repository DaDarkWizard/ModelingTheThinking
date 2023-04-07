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
    """
    [Summary]

    Parsers a scenario object from a CML definition.
    """

    tok = stack.pop()
    assert tok[0] == TokenType.IDENTIFIER,\
           "Scenario given without a valid name."

    new_scenario = Scenario(tok[1])

    while len(stack) > 1:

        tok = stack.pop()

        if tok[0] == TokenType.IDENTIFIER:
            if tok[1] == ":INDIVIDUALS":
                new_scenario.conditions = get_next_parentheses_unit(stack)

            elif tok[1] == ":INITIALLY":
                stack.pop()
                new_scenario.quantities = get_next_parentheses_unit(stack)

            elif tok[1] == ":THROUGHOUT":
                stack.pop()
                new_scenario.attributes = get_next_parentheses_unit(stack)

            elif tok[1] == ":BOUNDARY":
                new_scenario.consequences = get_next_parentheses_unit(stack)

            elif tok[1] == ":DOCUMENTATION":
                new_scenario.consequences = get_next_parentheses_unit(stack)

            elif tok[1] == ":SUBSTITUTIONS":
                new_scenario.consequences = get_next_parentheses_unit(stack)

            else:
                new_scenario.addons[tok[1]] = get_next_parentheses_unit(stack)

        else:
            raise Exception("Unknown element in scenario definition.")

    parser.scope.add_scenario(new_scenario)
