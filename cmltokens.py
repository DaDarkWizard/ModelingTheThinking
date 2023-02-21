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
    DEF_RELATION = 13
    DEF_QUANTITY_FUNCTION = 14
    DEF_MODEL_FRAGMENT = 15
    DEF_ENTITY = 16
    DEF_DIMENSION = 17
    DEF_UNIT = 18
    DEF_CONSTANT_QUANTITY = 19
    DEF_SCENARIO = 20
    
    DOCUMENTATION_ATTRIBUTE = 170

    FUNCTION_ATTRIBUTE = 180
    DIMENSION_ATTRIBUTE = 190


