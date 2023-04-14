from cmllexer import CMLLexer
from typing import List, Tuple
from cmltokens import TokenType
from cmlscope import CMLScope
from stackhelpers import get_rest_of_parentheses, get_lisp_quoted_list


class CMLParser:
    def parse_dimension(self, stack):
        from cmldimension import parse_dimension
        parse_dimension(self, stack)

    def parse_unit(self, stack):
        from cmlunit import parse_unit
        parse_unit(self, stack)

    def parse_relation(self, stack):
        from cmlrelation import parse_relation
        parse_relation(self, stack)

    def parse_modelfragment(self, stack):
        from cmlmodelfragment import parse_modelfragment
        parse_modelfragment(self, stack)
    
    def parse_quantityfunction(self, args):
        from cmlquantityfunction import parse_quantityfunction
        parse_quantityfunction(self, args)

    def parse_constantquantity(self, args):
        from cmlconstantquantity import parse_constantquantity
        parse_constantquantity(self, args)
    
    def parse_scenario(self, args):
        from cmlscenario import parse_scenario
        parse_scenario(self, args)

    def __init__(self, parser = None):
        self.input = ""
        self.lexer = CMLLexer()
        self.scope: CMLScope = CMLScope()
        self.builtin_functions = {}
        import cmlmath
        for k, v in cmlmath.init_math_functions().items():
            self.builtin_functions[k] = v

        if parser is not None:
            self.scope.parent = parser.scope

    def reset(self):
        self.scope = CMLScope()

    def parse_string(self, input_string: str):
        """[summary]

        Parses a string of cml into the model.

        ### Parameters
        1. input_string: str
           - The cml expression string to parse.
        """

        self.lexer.set_input(input_string)

        stack = self.lexer.lex_all()
        stack.reverse()

        return self.parse_stack(stack)

    def parse_stack(self, input_stack: List[Tuple[TokenType, any]]):
        """[summary]

        Parses a stack of cml tokens into the model.

        ### ParametersAre we still planning on having this done tomorrow night?
        1. input_stack: List[Tuple[TokenType, any]]
           - The cml expression stack to parse.
        """

        top_level = None

        tok = input_stack.pop()

        while True:

            if tok[0] == TokenType.LEFT_PARENTHESES:
                # Get the rest of everything enclosed in the parentheses.
                item_stack = get_rest_of_parentheses(input_stack)

                # Get the name of the function being called.
                func_name = item_stack.pop()

                # Remove the trailing parenthesis.
                item_stack.pop(0)

                # Handle the function.
                top_level = self.handle_func(func_name, item_stack)
            elif tok[0] == TokenType.QUOTE:
                return get_lisp_quoted_list(input_stack)
            elif tok[0] == TokenType.END:
                break
            else:
                raise Exception(f"Unknown value: {tok[0]}:{tok[1]}")

            if len(input_stack) == 0:
                break
            else:
                tok = input_stack.pop()

        return top_level


    def handle_func(self, func_name, args):
        if func_name[0] == TokenType.IDENTIFIER:
            if func_name[1] == "DEFDIMENSION":
                self.parse_dimension(args)
                return (TokenType.NIL, None)
            elif func_name[1] == "DEFUNIT":
                self.parse_unit(args)
                return (TokenType.NIL, None)
            elif func_name[1] == "DEFRELATION":
                self.parse_relation(args)
                return (TokenType.NIL, None)
            elif func_name[1] == "DEFMODELFRAGMENT":
                self.parse_modelfragment(args)
                return (TokenType.NIL, None)
            elif func_name[1] == "DEFCONSTANTQUANTITY":
                self.parse_constantquantity(args)
                return (TokenType.NIL, None)
            elif func_name[1] == "DEFQUANTITYFUNCTION":
                self.parse_quantityfunction(args)
                return (TokenType.NIL, None)
            elif func_name[1] == "DEFENTITY":
                self.parse_modelfragment(args)
                return (TokenType.NIL, None)
            elif func_name[1] == "DEFSCENARIO":
                self.parse_scenario(args)
                return (TokenType.NIL, None)
            else:
                raise Exception(f"Unknown function {func_name[1]}")
        else:
            raise Exception(f"Unknown function {func_name}")
