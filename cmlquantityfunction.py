"""
Handles all function for quantityfunction in CML
"""
from typing import List, Tuple
from cmltokens import TokenType
from cmlparser import CMLParser
from cmlclasses import Relation
from stackhelpers import get_next_parentheses_unit
from dimension import parse_dimension_expression

def parse_quantityfunction(parser: CMLParser,
                           stack: List[Tuple[TokenType, any]]):
    """
    [Summary]

    Parser a quantityfunction object from a CML definition.
    """
    tok = stack.pop()
    assert tok[0] == TokenType.IDENTIFIER,\
           "QuantityFunction given without a valid name."
    quant_func_args = get_next_parentheses_unit(stack)
    assert quant_func_args[-1][0] == TokenType.LEFT_PARENTHESES and\
           quant_func_args[0][0] == TokenType.RIGHT_PARENTHESES,\
           "Malformed relation args."
    quant_func_args.pop(0)
    quant_func_args.pop()
    new_quant_func = QuantityFunction(tok[1], quant_func_args)

    if stack[-1][0] == TokenType.IMPLICATION_ATTRIBUTE:
        stack.pop(0)
        new_quant_func.implication = get_next_parentheses_unit(stack)

    if stack[-1][0] == TokenType.DIMENSION_ATTRIBUTE:
        stack.pop(0)
        new_quant_func.dimension = parse_dimension_expression(parser, get_next_parentheses_unit(stack))

    if stack[-1][0] == TokenType.NON_NUMERIC_ATTRIBUTE:
