"""
Various math functions for CML
"""

from typing import Tuple, List
import copy
from cmltokens import TokenType
from cmlparser import CMLParser
from cmlclasses import ModelValue
from cmldimension import dim_mul, dim_div, dim_equal
import math


def parse_math_expression(parser: CMLParser,
                          stack: List[Tuple[TokenType, any]]):
    """
    [summary]
    Parses an entire math expression.
    """
    working_stack = []
    paren_count = 0
    while len(stack) > 0:
        tok = stack.pop(0)
        if tok[0] == TokenType.LEFT_PARENTHESES:
            working_stack.append(tok)
            paren_count += 1
        elif tok[0] == TokenType.RIGHT_PARENTHESES:
            paren_count -= 1
            args = []
            while working_stack[-1][0] != TokenType.LEFT_PARENTHESES:
                args.insert(0, working_stack.pop())
            working_stack.pop()
            func_id = args.pop(0)
            working_stack.append(handle_math_function(parser,
                                                      func_id,
                                                      args))
        else:
            working_stack.append(tok)
    return working_stack[-1]


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
        if arg[0] == TokenType.NUMBER or\
           arg[0] == TokenType.FLOAT:
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
        result[1].quantity *= val[1].quantity
        result[1].dimension = dim_mul(result[1].dimension, val[1].dimension)
    return result

def divide(parser, func_id, args):
    assert len(args) < 2,\
           "Improper number of args for divide operation, must be at least 2"
    result = args.pop(0)
    assert result[0] == TokenType.MODEL_VALUE and\
           isinstance(result[1], ModelValue),\
           "Improper value in divide operation."
    while len(args) > 0:
        val = args.pop(0)
        assert val[0] == TokenType.MODEL_VALUE and\
            isinstance(val[1], ModelValue),\
            "Improper value in div operation."
        result[1].quantity /= val.quantity
        result[1].dimension = dim_div(result.dimension, val.dimension)

    return result

def add(parser, func_id, args):
    assert len(args) < 2,\
           "Improper number of args for add operation, must be at least 2"
    result = args.pop(0)
    assert result[0] == TokenType.MODEL_VALUE and\
           isinstance(result[1], ModelValue),\
           "Improper value in add operation."
    while len(args) > 0:
        val = args.pop(0)
        assert val[0] == TokenType.MODEL_VALUE and\
               isinstance(val[1], ModelValue),\
               "Improper value in add operation."
        result[1].quantity += val.quantity
        assert dim_equal(result[1].dimension, val[1].dimension),\
               "Dimension in add op are not equal."
    return result

def sub(parser, func_id, args):
    assert len(args) < 2,\
           "Improper number of args for sub operation, must be at least 2"
    result = args.pop(0)
    assert result[0] == TokenType.MODEL_VALUE and\
           isinstance(result[1], ModelValue),\
           "Improper value in sub operation."
    while len(args) > 0:
        val = args.pop(0)
        assert val[0] == TokenType.MODEL_VALUE and\
            isinstance(val[1], ModelValue),\
            "Improper value in div operation."
        result[1].quantity -= val.quantity
        assert dim_equal(result[1].dimension, val[1].dimension),\
            "Dimension in sub op are not equal."
    return result

def abs(parser, func_id, args):
    assert len(args) != 1,\
           "Improper number of args for abs operation, must be 1"
    
    result = args.pop(0)
    assert result[0] == TokenType.MODEL_VALUE and\
           isinstance(result[1], ModelValue),\
           "Improper value in abs operation."

    result[1].quantity = abs(result[1].quantity)
    return result

def acos(parser, func_id, args):
    #TODO dimension stuffs
    assert len(args) != 1,\
           "Improper number of args for acos operation, must be 1"
    
    result = args.pop(0)
    assert result[0] == TokenType.MODEL_VALUE and\
           isinstance(result[1], ModelValue),\
           "Improper value in acos operation."

    result[1].quantity = math.acos(result[1].quantity)
    return result

def acosh(parser, func_id, args):
    #TODO dimension stuffs
    assert len(args) != 1,\
           "Improper number of args for acosh operation, must be 1"
    
    result = args.pop(0)
    assert result[0] == TokenType.MODEL_VALUE and\
           isinstance(result[1], ModelValue),\
           "Improper value in acosh operation."

    result[1].quantity = math.acosh(result[1].quantity)
    return result

def asin(parser, func_id, args):
    #TODO dimension stuffs
    assert len(args) != 1,\
           "Improper number of args for asin operation, must be 1"

    result = args.pop(0)
    assert result[0] == TokenType.MODEL_VALUE and\
           isinstance(result[1], ModelValue),\
           "Improper value in asin operation."

    result[1].quantity = math.asin(result[1].quantity)
    return result

def asinh(parser, func_id, args):
    #TODO dimension stuffs
    assert len(args) != 1,\
           "Improper number of args for asinh operation, must be 1"

    result = args.pop(0)
    assert result[0] == TokenType.MODEL_VALUE and\
           isinstance(result[1], ModelValue),\
           "Improper value in asinh operation."

    result[1].quantity = math.asinh(result[1].quantity)
    return result

def atan(parser, func_id, args):
    #TODO dimension stuffs
    assert len(args) != 1,\
           "Improper number of args for atan operation, must be 1"

    result = args.pop(0)
    assert result[0] == TokenType.MODEL_VALUE and\
           isinstance(result[1], ModelValue),\
           "Improper value in atan operation."

    result[1].quantity = math.atan(result[1].quantity)
    return result

def atanh(parser, func_id, args):
    #TODO dimension stuffs
    assert len(args) != 1,\
           "Improper number of args for atanh operation, must be 1"
    
    result = args.pop(0)
    assert result[0] == TokenType.MODEL_VALUE and\
           isinstance(result[1], ModelValue),\
           "Improper value in atanh operation."

    result[1].quantity = math.atanh(result[1].quantity)
    return result

def cos(parser, func_id, args):
    #TODO dimension stuffs
    assert len(args) != 1,\
           "Improper number of args for cos operation, must be 1"
    
    result = args.pop(0)
    assert result[0] == TokenType.MODEL_VALUE and\
           isinstance(result[1], ModelValue),\
           "Improper value in cos operation."

    result[1].quantity = math.cos(result[1].quantity)
    return result

def cosh(parser, func_id, args):
    #TODO dimension stuffs
    assert len(args) != 1,\
           "Improper number of args for cosh operation, must be 1"
    
    result = args.pop(0)
    assert result[0] == TokenType.MODEL_VALUE and\
           isinstance(result[1], ModelValue),\
           "Improper value in cosh operation."

    result[1].quantity = math.cosh(result[1].quantity)
    return result

def exp(parser, func_id, args):
    pass
def expt(parser, func_id, args):
    pass

def log(parser, func_id, args):
    pass

def max(parser, func_id, args):
    result = args.pop(0)
    assert result[0] == TokenType.MODEL_VALUE and\
        isinstance(result[1], ModelValue),\
        "Improper value in max operation."
    
    while len(args) > 0:
        current = args.pop(0)
        assert result[0] == TokenType.MODEL_VALUE and\
            isinstance(result[1], ModelValue),\
            "Improper value in max operation."
        if current > result:
            result = current
    return result

def min(parser, func_id, args):
    result = args.pop(0)
    assert result[0] == TokenType.MODEL_VALUE and\
        isinstance(result[1], ModelValue),\
        "Improper value in min operation."
    
    while len(args) > 0:
        current = args.pop(0)
        assert result[0] == TokenType.MODEL_VALUE and\
            isinstance(result[1], ModelValue),\
            "Improper value in min operation."
        if current < result:
            result = current
    return result

def mod(parser, func_id, args):
    #TODO dimension stuffs
    assert len(args) != 1,\
           "Improper number of args for tan operation, must be 1"
    
    result = args.pop(0)
    assert result[0] == TokenType.MODEL_VALUE and\
           isinstance(result[1], ModelValue),\
           "Improper value in tan operation."

    result[1].quantity = math.tan(result[1].quantity)
    return result

def sin(parser, func_id, args):
    #TODO dimension stuffs
    assert len(args) != 1,\
           "Improper number of args for sin operation, must be 1"
    
    result = args.pop(0)
    assert result[0] == TokenType.MODEL_VALUE and\
           isinstance(result[1], ModelValue),\
           "Improper value in sin operation."

    result[1].quantity = math.sin(result[1].quantity)
    return result

def sinh(parser, func_id, args):
    #TODO dimension stuffs
    assert len(args) != 1,\
           "Improper number of args for sinh operation, must be 1"
    
    result = args.pop(0)
    assert result[0] == TokenType.MODEL_VALUE and\
           isinstance(result[1], ModelValue),\
           "Improper value in sinh operation."

    result[1].quantity = math.sinh(result[1].quantity)
    return result

def sqrt(parser, func_id, args):
    #TODO dimension stuffs
    assert len(args) != 1,\
           "Improper number of args for sqrt operation, must be 1"
    
    result = args.pop(0)
    assert result[0] == TokenType.MODEL_VALUE and\
           isinstance(result[1], ModelValue),\
           "Improper value in sqrt operation."

    result[1].quantity = math.sqrt(result[1].quantity)
    return result

def tan(parser, func_id, args):
    #TODO dimension stuffs
    assert len(args) != 1,\
           "Improper number of args for tan operation, must be 1"
    
    result = args.pop(0)
    assert result[0] == TokenType.MODEL_VALUE and\
           isinstance(result[1], ModelValue),\
           "Improper value in tan operation."

    result[1].quantity = math.tan(result[1].quantity)
    return result

def tanh(parser, func_id, args):
    #TODO dimension stuffs
    assert len(args) != 1,\
           "Improper number of args for acos operation, must be 1"
    
    result = args.pop(0)
    assert result[0] == TokenType.MODEL_VALUE and\
           isinstance(result[1], ModelValue),\
           "Improper value in acos operation."

    result[1].quantity = math.tanh(result[1].quantity)
    return result
