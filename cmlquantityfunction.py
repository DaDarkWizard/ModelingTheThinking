"""
Handles all function for quantityfunction in CML
"""
from typing import List, Tuple
from cmltokens import TokenType
from cmlparser import CMLParser
from cmlclasses import QuantityFunction
from stackhelpers import get_next_parentheses_unit
from cmldimension import parse_dimension_expression

def parse_quantityfunction(parser: CMLParser,
                           args: List[Tuple[TokenType, any]]):
    """
    [Summary]

    Parser a quantityfunction object from a CML definition.
    """
    tok = args.pop()
    assert tok[0] == TokenType.IDENTIFIER,\
           "QuantityFunction given without a valid name."
    quant_func_args = get_next_parentheses_unit(args)
    assert quant_func_args[-1][0] == TokenType.LEFT_PARENTHESES and\
           quant_func_args[0][0] == TokenType.RIGHT_PARENTHESES,\
           "Malformed relation args."
    quant_func_args.pop(0)
    quant_func_args.pop()
    new_quant_func = QuantityFunction(tok[1], quant_func_args)


    while len(args) > 0:

        tok = args.pop()

        if tok[0] == TokenType.IDENTIFIER:
            if tok[1] == ":=>":
                new_quant_func.implication = get_next_parentheses_unit(args)
            elif tok[1] == ":DIMENSION":
                new_quant_func.dimension = parse_dimension_expression(parser, get_next_parentheses_unit(args))
            elif tok[1] == ":NON-NUMERIC":
                new_quant_func.non_numeric = get_next_parentheses_unit(args)
            elif tok[1] == ":PIECEWISE-CONTINUOUS":
                new_quant_func.piecewise_continuous = get_next_parentheses_unit(args)
            elif tok[1] == ":STEP-QUANTITY":
                new_quant_func.non_numeric = get_next_parentheses_unit(args)
            elif tok[1] == ":COUNT-QUANTITY":
                new_quant_func.count_quantity = get_next_parentheses_unit(args)
            else:
                new_quant_func.addons[tok[1]] = get_next_parentheses_unit(args)
        else:
            raise Exception(f"Invalid definition for QuantityFunction {new_quant_func.name}")
    
    parser.scope.add_quantityfunction(new_quant_func)

