"""
Handles parsing and creation of macros.
"""
from stackhelpers import get_next_parentheses_unit
from lispclasses import Macro
from cmltokens import TokenType
from cmlparser import CMLParser


def lisp_def_macro(parser, name, args):
    """
    [Summary]

    Function to handle the creation of a macro.
    Macros are special functions that do not evaluate their arguments.
    """
    macro_name = get_next_parentheses_unit(args)

    assert macro_name[0] == TokenType.IDENTIFIER,\
        "Macro name too complex."

    result = Macro(macro_name[1])

    variable_names = get_next_parentheses_unit(args)
    variable_names.pop(0)
    variable_names.pop()

    while len(variable_names) > 0:
        result.args.append(variable_names.pop())

    result.code = get_next_parentheses_unit(args)

    parser.scope.set_lispobject(result.name, (TokenType.MACRO, result))


def lisp_call_macro(parser, macro: Macro, args):
    """
    [Summary]

    Function to handle calling a macro.
    Sets the arguments as code objects and does its thing.
    """
    arg_vals = {}
    for name in macro.args:
        if len(args) > 0:
            arg_vals[name] = (TokenType.RAW_CODE,
                              get_next_parentheses_unit(args))
        else:
            arg_vals[name] = []
            arg_vals[name].append((TokenType.NIL, None))

    result = macro.code.copy()
    parser = CMLParser(parser)

    for k, v in arg_vals:
        parser.scope.set_lispobject(k, v)

    result = parser.parse_stack(result)

    return result
