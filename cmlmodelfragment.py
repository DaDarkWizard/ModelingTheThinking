"""
Handles all functions for modelfragment in CML
"""
from typing import List, Tuple
from cmltokens import TokenType
from cmlparser import CMLParser
from cmlclasses import ModelFragment
from stackhelpers import get_next_parentheses_unit


def parse_modelfragment(parser: CMLParser,
                        stack: List[Tuple[TokenType, any]]):
    """
    [Summary]

    Parsers a modelfragment object from a CML definition.
    """
    tok = stack.pop()
    assert tok[0] == TokenType.IDENTIFIER,\
           "ModelFragment given without a valid name."

    new_model = ModelFragment(tok[1])
    if stack[-1][0] == TokenType.DOCUMENTATION_ATTRIBUTE:
        stack.pop()
        new_model.documentation = stack.pop(0)[1]

    if stack[-1][0] == TokenType.IMPLICATION_ATTRIBUTE:
        stack.pop()
        new_model.implication = get_next_parentheses_unit(stack)

    if stack[-1][0] == TokenType.SUBCLASS_OF_ATTRIBUTE:
        stack.pop()
        new_model.sub_class_of = get_next_parentheses_unit(stack)

    if stack[-1][0] == TokenType.PARTICIPANTS_ATTRIBUTE:
        stack.pop()
        new_model.participants = get_next_parentheses_unit(stack)

    if stack[-1][0] == TokenType.IDENTIFIER and\
       stack[-1][1] == ":conditions":
        stack.pop()
        new_model.conditions = get_next_parentheses_unit(stack)

    if stack[-1][0] == TokenType.IDENTIFIER and\
       stack[-1][1] == ":quantities":
        stack.pop()
        new_model.quantities = get_next_parentheses_unit(stack)

    if stack[-1][0] == TokenType.IDENTIFIER and\
       stack[-1][1] == ":attributes":
        stack.pop()
        new_model.attributes = get_next_parentheses_unit(stack)

    if stack[-1][0] == TokenType.IDENTIFIER and\
       stack[-1][1] == ":consequences":
        new_model.consequences = get_next_parentheses_unit(stack)

    parser.scope.add_modelfragment(new_model)
