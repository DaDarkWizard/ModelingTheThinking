"""
Handles all functions for relations in CML
"""
from typing import List, Tuple
from cmltokens import TokenType
from cmlparser import CMLParser
from cmlclasses import Relation
from stackhelpers import get_next_parentheses_unit


def parse_relation(parser: CMLParser,
                   args: List[Tuple[TokenType, any]]):
    """
    [Summary]

    Parses a relation object from a CML definition.

    """
    tok = args.pop()
    assert tok[0] == TokenType.IDENTIFIER,\
           "Relation given without a valid name."
    rel_args = get_next_parentheses_unit(args)
    assert rel_args[-1][0] == TokenType.LEFT_PARENTHESES and\
           rel_args[0][0] == TokenType.RIGHT_PARENTHESES,\
           "Malformed relation args."
    rel_args.pop(0)
    rel_args.pop()
    new_relation = Relation(tok[1], rel_args)

    while len(args) > 0:

        tok = args.pop()

        if tok[0] == TokenType.IDENTIFIER:

            if tok[1] == ":=>":
                new_relation.implication = get_next_parentheses_unit(args)

            elif tok[1] == ":<=>":
                new_relation.iff = get_next_parentheses_unit(args)

            elif tok[1] == ":FUNCTION":
                tok = args.pop()
                new_relation.function = (tok[1].lower() == "t")

            elif tok[1] == ":TIME-DEPENDENT":
                tok = args.pop()
                new_relation.time_dependent = (tok[1].lower() == "t")
            else:
                new_relation.addons[tok[1]] = get_next_parentheses_unit(args)
        else:
            raise Exception(f"Invalid relation definition for {new_relation.name}")

    parser.scope.add_relation(new_relation)
