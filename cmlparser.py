from cmllexer import *
from typing import List, Tuple
from cmltokens import *
from cmlscope import *
from stackhelpers import *
import cmldimension

class CMLParser:
    def __init__(self):
        self.input = ""
        self.lexer = CMLLexer()
        self.scope = CMLScope()

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

        self.parse_stack(stack)
    
    def parse_stack(self, input_stack: List[Tuple[TokenType, any]]):
        """[summary]

        Parses a stack of cml tokens into the model.

        ### ParametersAre we still planning on having this done tomorrow night?
        1. input_stack: List[Tuple[TokenType, any]]
           - The cml expression stack to parse.
        """

        tok = input_stack.pop()

        while True:

            if tok[0] == TokenType.DEF_DIMENSION:
                self.scope.stack.pop()
                dimension_stack = get_rest_of_parentheses(input_stack)
                cmldimension.parse_dimension(self, dimension_stack)
            else:
                self.scope.stack.append(tok[0])



            if len(input_stack) == 0:
                break
            else:
                tok = input_stack.pop()