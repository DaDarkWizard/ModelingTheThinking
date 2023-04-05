from cmltokens import TokenType

# Allows type hinting for lambda functions
from typing import Callable
from typing import List, Tuple

import re


class LexRule:
    """[summary]

    The LexRule class. Defines a regular expression to search for, the TokenType of the string if found, and a function to get the value from the string.

    """

    def __init__(self, regex_string: str, token_type: TokenType, value_function: Callable[[str], any], skip: bool = False):
        """[summary]

        ### Parameters
        1. regex_string: str
           - The regular expression string used to match this rule.
        2. token_type: TokenType
           - The type of this token
        3. value_function: (str) -> Any
           - The function to return a value from the raw regex matched string
        """
        self.regex_string = regex_string
        self.token_type = token_type
        self.value_function = value_function
        self.skip = skip


class Lexer:
    """[summary]

    The main Lexer class. Handles converting a textual input into tokens.

    """

    def __init__(self):
        self.input_text = ""
        self.input_index = 0
        self.regexes: List[LexRule] = list()
        self.end_token = None


    def set_input(self, input: str):
        self.input_index = 0
        self.input_text = input


    def add_regex(self, new_rule: LexRule):
        self.regexes.append(new_rule)

    def lex(self):
        if(self.input_index >= len(self.input_text)):
            return (TokenType.END, None)

        for rule in self.regexes:
            m = re.match(rule.regex_string, self.input_text[self.input_index:])
            if m is not None:
                matched_string = self.input_text[self.input_index:self.input_index + m.end() ]
                self.input_index += m.end()
                if rule.skip:
                    return self.lex()
                else:
                    if rule.value_function is None:
                        return (rule.token_type, None)
                    else:
                        return (rule.token_type, rule.value_function(matched_string))

        raise Exception("Could not parse to end of input")

    def lex_all(self):

        token_list: List[Tuple[TokenType, any]] = list()

        while self.input_index < len(self.input_text):
            token = self.lex()
            if token is None:
                break
            else:
                token_list.append(token)

        return token_list

class CMLLexer(Lexer):
    def __init__(self):
        Lexer.__init__(self)
        self.add_regex(LexRule(r'\s+', None, None, skip=True))

        self.add_regex(LexRule(r'defRelation', TokenType.DEF_RELATION, None))
        self.add_regex(LexRule(r'defQuantityFunction',
                               TokenType.DEF_QUANTITY_FUNCTION, None))
        self.add_regex(LexRule(r'defModelFragment',
                               TokenType.DEF_MODEL_FRAGMENT, None))
        self.add_regex(LexRule(r'defEntity', TokenType.DEF_ENTITY, None))
        self.add_regex(LexRule(r'defDimension', TokenType.DEF_DIMENSION, None))
        self.add_regex(LexRule(r'defUnit', TokenType.DEF_UNIT, None))
        self.add_regex(LexRule(r'defConstantQuantity',
                               TokenType.DEF_CONSTANT_QUANTITY, None))
        self.add_regex(LexRule(r'defScenario', TokenType.DEF_SCENARIO, None))
        self.add_regex(LexRule(r':documentation',
                               TokenType.DOCUMENTATION_ATTRIBUTE, None))
        self.add_regex(LexRule(r':dimension',
                               TokenType.DIMENSION_ATTRIBUTE, None))
        self.add_regex(LexRule(r':non-numeric',
                               TokenType.NON_NUMERIC_ATTRIBUTE, None))
        self.add_regex(LexRule(r':piecewise-continuous',
                               TokenType.PIECEWISE_CONTINUOUS_ATTRIBUTE, None))
        self.add_regex(LexRule(r':step-quantity',
                               TokenType.STEP_QUANTITY_ATTRIBUTE, None))
        self.add_regex(LexRule(r':count-quantity',
                               TokenType.COUNT_QUANTITY_ATTRIBUTE, None))
        self.add_regex(LexRule(r':subclass-of',
                               TokenType.SUBCLASS_OF_ATTRIBUTE, None))
        self.add_regex(LexRule(r':participants',
                               TokenType.PARTICIPANTS_ATTRIBUTE, None))
        self.add_regex(LexRule(r':=>', TokenType.IMPLICATION_ATTRIBUTE, None))
        self.add_regex(LexRule(r':<=>', TokenType.IFF_ATTRIBUTE, None))
        self.add_regex(LexRule(r':=', TokenType.ASSIGNMENT_ATTRIBUTE, None))
        self.add_regex(LexRule(r':time-dependent',
                               TokenType.TIME_DEPENDENT_ATTRIBUTE,
                               None))
        self.add_regex(LexRule(r':function',
                               TokenType.FUNCTION_ATTRIBUTE,
                               None))
        self.add_regex(LexRule(r'\+', TokenType.PLUS, None))
        self.add_regex(LexRule(r'-', TokenType.MINUS, None))
        self.add_regex(LexRule(r'\*', TokenType.STAR, None))
        self.add_regex(LexRule(r'/', TokenType.DIVIDE, None))
        self.add_regex(LexRule(r'expt', TokenType.EXPT, None))


        self.add_regex(LexRule(r'\(', TokenType.LEFT_PARENTHESES, None))
        self.add_regex(LexRule(r'\)', TokenType.RIGHT_PARENTHESES, None))
        self.add_regex(LexRule(r'[1-9][0-9]*(?=[\s\)]|$)', TokenType.INTEGER, lambda x: int(x)))
        self.add_regex(LexRule(r'[0-9]+\.[0-9]+(?=[\s\)])', TokenType.FLOAT, lambda x: float(x)))
        self.add_regex(LexRule(r'\"(\\\"|[^\"])*\"|\'(\\\'|[^\'])*\'', TokenType.STRING, lambda x: x[1:-1]))
        self.add_regex(LexRule(r'[nN][iI][lL](?=[^\s]|\))', TokenType.NIL, None))

        # Comments?
        self.add_regex(LexRule(r'#([^\r])*\r', TokenType.COMMENT, None))

        self.add_regex(LexRule(r'[^\s\)]+', TokenType.IDENTIFIER, lambda x: x))



#
#(defRelation contents (?x ?y)
# :=> (and (container ?x)
# (contained-stuff ?y))
# :<=> (contained-in ?y ?x))
#
# (=> (contents "box" "spoons") (and (container ?x) (contained-stuff ?y)) )
#
#
#
