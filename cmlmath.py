"""
Various math functions for CML
"""

from typing import Tuple, List
import copy
from cmltokens import TokenType
from cmlparser import CMLParser
from cmlclasses import ModelValue
from cmldimension import dim_mul, dim_div, dim_equal


def handle_math_function(parser: CMLParser,
                         func_id: Tuple[TokenType, any],
                         args: List[Tuple[TokenType, any]]):
    """
    Handles parsing a simple math function in CML.
    """

    # First we need to clean the arguments
    for i, arg in enumerate(args):
        if arg[0] == TokenType.IDENTIFIER:
            # If this is an identifier, we should replace it with a value.
            new_arg = ModelValue()

            if arg[1] in parser.scope.dimensions():
                new_arg.quantity = 1
                new_arg.dimension = parser.scope.get_dimension(arg[1])\
                                          .dimension.copy()
            elif arg[1] in parser.scope.units():
                new_arg = copy.deepcopy(parser.scope.get_unit(arg[1]).value)
            else:
                raise Exception("Failed to replace identifier " +
                                "while parsing math expression.")

            args[i] = (TokenType.MODEL_VALUE, new_arg)
        if arg[0] == TokenType.NUMBER:
            new_arg = ModelValue()
            new_arg.quantity = arg[1]
            new_arg.dimension = {}
            args[i] = (TokenType.MODEL_VALUE, new_arg)

    func_call = None

    if func_id[0] == TokenType.STAR:
        func_call = star
    elif func_id[0] == TokenType.DIVIDE:
        func_call = divide
    elif func_id[0] == TokenType.PLUS:
        func_call = add
    elif func_id[0] == TokenType.MINUS:
        func_call = sub
    else:
        raise Exception("Not Implemented")

    return func_call(parser, func_id, args)


def star(parser, func_id, args):
    result = args.pop(0)
    assert result[0] == TokenType.MODEL_VALUE and\
           isinstance(result[1], ModelValue),\
           "Improper value in star operation."
    while len(args) > 0:
        val = args.pop(0)
        assert val[0] == TokenType.MODEL_VALUE and\
               isinstance(val[1], ModelValue),\
               "Improper value in star operation."
        result[1].quantity *= val.quantity
        result[1].dimension = dim_mul(result.dimension, val.dimension)
    return result


def divide(parser, func_id, args):
    result = args.pop(0)
    assert result[0] == TokenType.MODEL_VALUE and\
           isinstance(result[1], ModelValue),\
           "Improper value in star operation."
    assert len(args) == 2,\
           "Arg count for divide op must be 2"
    val = args.pop(0)
    assert val[0] == TokenType.MODEL_VALUE and\
           isinstance(val[1], ModelValue),\
           "Improper value in div operation."
    result[1].quantity /= val.quantity
    result[1].dimension = dim_div(result.dimension, val.dimension)
    return result


def add(parser, func_id, args):
    result = args.pop(0)
    assert result[0] == TokenType.MODEL_VALUE and\
           isinstance(result[1], ModelValue),\
           "Improper value in star operation."
    while len(args) > 0:
        val = args.pop(0)
        assert val[0] == TokenType.MODEL_VALUE and\
               isinstance(val[1], ModelValue),\
               "Improper value in star operation."
        result[1].quantity += val.quantity
        assert dim_equal(result[1].dimension, val[1].dimension),\
               "Dimension in add op are not equal."
    return result


def sub(parser, func_id, args):
    result = args.pop(0)
    assert result[0] == TokenType.MODEL_VALUE and\
           isinstance(result[1], ModelValue),\
           "Improper value in star operation."
    assert len(args) == 2,\
           "Arg count for divide op must be 2"
    val = args.pop(0)
    assert val[0] == TokenType.MODEL_VALUE and\
           isinstance(val[1], ModelValue),\
           "Improper value in div operation."
    result[1].quantity -= val.quantity
    assert dim_equal(result[1].dimension, val[1].dimension),\
           "Dimension in add op are not equal."
    return result
