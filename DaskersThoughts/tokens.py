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

class Token:
    def __init__(self, type: TokenType, value):
        self.type = type
        self.value = value