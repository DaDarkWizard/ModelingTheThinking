from cmlclasses import CMLObject
from cmltokens import TokenType
from stackhelpers import get_next_parentheses_unit
from cmlparser import CMLParser

def create_cmlobject(parser: CMLParser, stack):
    if stack[-1][0] == TokenType.LEFT_PARENTHESES:
        stack.pop()
        stack.pop(0)

    tok = stack.pop()
    assert tok[0] == TokenType.IDENTIFIER,\
        f"Invalid individual"
    indiv = CMLObject(tok[1])

    while len(stack) > 0:

        tok = stack.pop()

        if tok[0] == TokenType.IDENTIFIER:
            if tok[1] == ":TYPE":
                indiv.type = get_next_parentheses_unit(stack)[1]
                assert indiv.type in parser.scope.modelfragments(),\
                    f"Type {indiv.type} does not exist in object creation."
            else:
                indiv.addons[tok[1]] = get_next_parentheses_unit(stack)
        else:
            raise Exception(f"Invalid individual definition for {indiv.name}")
    
    ob_class = parser.scope.modelfragments()[indiv.type]

    def initialize_class(indiv, cls):
        for sub_cls in cls.sub_class_of:
            initialize_class(indiv, parser.scope.modelfragments()[sub_cls[1]])

    initialize_class(indiv, ob_class)

    parser.scope.add_cmlobject(indiv)
    return indiv