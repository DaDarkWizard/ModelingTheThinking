from cmllexer import CMLLexer
from typing import List, Tuple
from cmltokens import TokenType
from cmlscope import CMLScope
from stackhelpers import get_rest_of_parentheses


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

    def __init__(self):
        self.input = ""
        self.lexer = CMLLexer()
        self.scope: CMLScope = CMLScope()

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
                self.parse_dimension(dimension_stack)
            elif tok[0] == TokenType.DEF_UNIT:
                self.scope.stack.pop()
                unit_stack = get_rest_of_parentheses(input_stack)
                self.parse_unit(unit_stack)
            elif tok[0] == TokenType.DEF_RELATION:
                self.scope.stack.pop()
                unit_stack = get_rest_of_parentheses(input_stack)
                self.parse_relation(unit_stack)
            elif tok[0] == TokenType.DEF_MODEL_FRAGMENT:
                self.scope.stack.pop()
                unit_stack = get_rest_of_parentheses(input_stack)
                self.parse_modelfragment(unit_stack)
            else:
                self.scope.stack.append(tok[0])

            if len(input_stack) == 0:
                break
            else:
                tok = input_stack.pop()
