"""
Handles all functions for modelfragment in CML
"""
from typing import List, Tuple
from cmltokens import TokenType
from cmlparser import CMLParser
from cmlclasses import ModelFragment
from stackhelpers import get_next_parentheses_unit


def parse_modelfragment(parser: CMLParser,
                        args: List[Tuple[TokenType, any]]):
    """
    [Summary]

    Parsers a modelfragment object from a CML definition.
    """
    tok = args.pop()
    assert tok[0] == TokenType.IDENTIFIER,\
           "ModelFragment given without a valid name."

    new_model = ModelFragment(tok[1])

    while len(args) > 0:

        tok = args.pop()

        if tok[0] == TokenType.IDENTIFIER:

            
            
            if tok[1] == ":SUBCLASS-OF":
                subclassstack = get_next_parentheses_unit(args)
                subclassstack.pop()
                subclassstack.pop(0)
                for cls in subclassstack:
                    assert cls[1] in parser.scope.modelfragments(),\
                        f"Fragment {cls[1]} undefined when defining {new_model.name} ModelFragment"
                new_model.sub_class_of = subclassstack

            elif tok[1] == ":PARTICIPANTS":
                new_model.participants = get_next_parentheses_unit(args)

            elif tok[1] == ":CONDITIONS":
                new_model.conditions = get_next_parentheses_unit(args)

            elif tok[1] == ":QUANTITIES":
                new_model.quantities = get_next_parentheses_unit(args)

            elif tok[1] == ":ATTRIBUTES":
                new_model.attributes = get_next_parentheses_unit(args)

            elif tok[1] == ":CONSEQUENCES":
                new_model.consequences = get_next_parentheses_unit(args)
            
            elif tok[1] == ":DOCUMENTATION":
                new_model.documentation = args.pop(0)[1]
            
            elif tok[1] == ":SUBSTITUTIONS":
                new_model.substitutions = get_next_parentheses_unit(args)
            
            else:
                property_name = tok[1]
                new_model.addons[property_name] = get_next_parentheses_unit(args)
        else:
            raise Exception(f"Invalid unit definition for {new_model.name}")

    parser.scope.add_modelfragment(new_model)
