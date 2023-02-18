from enum import Enum

class TokenType(Enum):

    # Base tokens
    LEFT_PARENTHESES = 1
    RIGHT_PARENTHESES = 2
    INTEGER = 3
    FLOAT = 4
    STRING = 5
    IDENTIFIER = 6
    WHITESPACE = 7
    END = 8
    NUMBER = 9
    CONS = 10
    NIL = 11
    TRUE = 12
