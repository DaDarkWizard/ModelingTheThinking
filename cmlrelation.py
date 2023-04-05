"""
Handles all functions for relations in CML
"""
from typing import List, Tuple
from cmltokens import TokenType
from cmlparser import CMLParser
from cmlclasses import Relation
from stackhelpers import get_next_parentheses_unit


def parse_relation(parser: CMLParser,
                   stack: List[Tuple[TokenType, any]]):
    """
    [Summary]

    Parses a relation object from a CML definition.

    """
    tok = stack.pop()
    assert tok[0] == TokenType.IDENTIFIER,\
           "Relation given without a valid name."
    rel_args = get_next_parentheses_unit(stack)
    assert rel_args[-1][0] == TokenType.LEFT_PARENTHESES and\
           rel_args[0][0] == TokenType.RIGHT_PARENTHESES,\
           "Malformed relation args."
    rel_args.pop(0)
    rel_args.pop()
    new_relation = Relation(tok[1], rel_args)

    if stack[-1][0] == TokenType.IMPLICATION_ATTRIBUTE:
        stack.pop()
        new_relation.implication = get_next_parentheses_unit(stack)

    if stack[-1][0] == TokenType.IFF_ATTRIBUTE:
        stack.pop()
        new_relation.iff = get_next_parentheses_unit(stack)

    if stack[-1][0] == TokenType.FUNCTION_ATTRIBUTE:
        stack.pop()
        tok = stack.pop()
        new_relation.function = (tok[1].lower() == "t")

    if stack[-1][0] == TokenType.TIME_DEPENDENT_ATTRIBUTE:
        stack.pop()
        tok = stack.pop()
        new_relation.time_dependent = (tok[1].lower() == "t")

    parser.scope.add_relation(new_relation)
