"""
Handles all functions for modelfragment in CML
"""
from typing import List, Tuple
from cmltokens import TokenType
from cmlparser import CMLParser
from cmlclasses import Scenario, CMLObject
from stackhelpers import get_next_parentheses_unit
from cmlobject import create_cmlobject


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
                indivs = get_next_parentheses_unit(stack)
                indivs.pop()
                indivs.pop(0)
                while len(indivs) > 0:
                    indiv = create_cmlobject(parser, get_next_parentheses_unit(indivs))
                    new_scenario.individuals[indiv.name] = indiv

            elif tok[1] == ":INITIALLY":
                stack.pop()
                new_scenario.initially = get_next_parentheses_unit(stack)

            elif tok[1] == ":THROUGHOUT":
                throughs = get_next_parentheses_unit(stack)
                throughs.pop()
                throughs.pop(0)
                while len(throughs) > 0:
                    through = get_next_parentheses_unit(throughs)
                    new_scenario.throughout.append(through)

            elif tok[1] == ":BOUNDARY":
                new_scenario.boundary = get_next_parentheses_unit(stack)

            elif tok[1] == ":DOCUMENTATION":
                new_scenario.documentation = get_next_parentheses_unit(stack)

            elif tok[1] == ":SUBSTITUTIONS":
                new_scenario.substitutions = get_next_parentheses_unit(stack)

            else:
                new_scenario.addons[tok[1]] = get_next_parentheses_unit(stack)

        else:
            raise Exception("Unknown element in scenario definition.")
    
    if len(new_scenario.throughout) > 0:
        for parse_list in new_scenario.throughout:
            deps = []
            for i in range(len(parse_list) - 1, -1, -1):
                if parse_list[i][0] == TokenType.IDENTIFIER and\
                   parse_list[i][1] in new_scenario.individuals.keys():
                    deps.insert(0, parse_list[i][1])
            if len(deps) > 1:
                elem = deps.pop()
                new_scenario.individuals[elem].depends.update(deps)
                


    parser.scope.add_scenario(new_scenario)
