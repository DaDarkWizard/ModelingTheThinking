from stackhelpers import *
from cmlclasses import Dimension
import cmlparser

def parse_dimension(parser: cmlparser.CMLParser, stack):
    """[summary]

        Parses a stack containing a dimension description.

        The stack will come in without the first parentheses or def-dimension.

        ### Parameters
        1. parser: CMLParser
           - The cml parser we are using.
        2. stack: List[Tuple[TokenType, any]]
           - The stack to parse the dimension from.
    """

    tok = stack.pop()
    assert tok[0] == TokenType.IDENTIFIER, "Dimension given without a name"
    new_dim = Dimension(tok[1])
    assert new_dim.name not in parser.scope.dimensions, f"Dimension {new_dim.name} already exists"
    tok = stack.pop()

    if tok[0] == TokenType.DOCUMENTATION_ATTRIBUTE:
        tok = stack.pop()
        assert tok[0] == TokenType.STRING, "Documentation attribute given without string"
        new_dim.documentation = tok[1]
        tok = stack.pop()
    
    if tok[0] == TokenType.RIGHT_PARENTHESES:
        new_dim.dimension[new_dim.name] = 1
        parser.scope.dimensions[new_dim.name] = new_dim
    else:
        assert tok[0] == TokenType.ASSIGNMENT_ATTRIBUTE, "Invalid dimension expression"
        dimension_expression = get_next_parentheses_unit(stack)
        new_dim.dimension = parse_dimension_expression(parser, dimension_expression)[1]

        # We do a little clean-up
        for name, value in new_dim.dimension.items():
            if value == 0:
                del new_dim.dimension[name]
        
        # Ensure each dimension is only defined once.
        for old_dim_name, old_dim in parser.scope.dimensions.items():
            all_equal = True
            for item_name, number in new_dim.dimension.items():
                if item_name not in old_dim.dimension or number != old_dim.dimension[item_name]:
                    all_equal = False
                    break
            if all_equal:
                raise Exception(f"Dimension {old_dim_name} defined twice! Second: {new_dim.name}")
        
        # Add the dimension to the parser.
        parser.scope.dimensions[new_dim.name] = new_dim
    
    return

def parse_dimension_expression(parser, stack):

    working_stack = list()
    paren_count = 0

    def identifier_to_dimension(id):
        assert id[0] == TokenType.IDENTIFIER, "Invalid dimension given"
        assert id[1] in parser.scope.dimensions, "Undefined dimension in dimension definision"
        #dim_value = dict()
        #dim_value[id[1]] = 1
        return (TokenType.DIMENSION_VALUE, parser.scope.dimensions[id[1]].dimension.copy())

    print(list(map(lambda x: x[0], stack)))

    while len(stack) > 0:
        tok = stack.pop()
        if tok[0] == TokenType.LEFT_PARENTHESES:
            paren_count += 1
            working_stack.append(tok)
        elif tok[0] == TokenType.RIGHT_PARENTHESES:
            paren_count -= 1
            args = list()
            arg2 = working_stack.pop()
            if arg2[0] == TokenType.IDENTIFIER:
                arg2 = identifier_to_dimension(arg2)
            arg1 = working_stack.pop()
            if arg1[0] == TokenType.IDENTIFIER:
                arg1 = identifier_to_dimension(arg1)
            elif arg1[0] == TokenType.LEFT_PARENTHESES:
                working_stack.append(arg2)
                continue

            func = working_stack.pop()
            if func[0] == TokenType.STAR:
                for name, value in arg2[1].items():
                    if name in arg1[1]:
                        arg1[1][name] += value
                    else:
                        arg1[1][name] = value
            elif func[0] == TokenType.DIVIDE:
                for name, value in arg2[1].items():
                    if name in arg1[1]:
                        arg1[1][name] -= value
                    else:
                        arg1[1][name] = -1 * value
            elif func[0] == TokenType.EXPT:
                for name, value in arg1[1].items():
                    arg1[1][name] = value * arg2[1]
            else:
                raise Exception("Invalid dimension expression")
            
            working_stack.append(arg1)

            if paren_count == 0:
                return working_stack.pop()
        else:
            working_stack.append(tok)

    return working_stack.pop()
