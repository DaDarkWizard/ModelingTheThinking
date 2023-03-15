from stackhelpers import TokenType, get_next_parentheses_unit
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
    assert new_dim.name not in parser.scope.dimensions,\
           f"Dimension {new_dim.name} already exists"
    tok = stack.pop()

    if tok[0] == TokenType.DOCUMENTATION_ATTRIBUTE:
        tok = stack.pop()
        assert tok[0] == TokenType.STRING,\
               "Documentation attribute given without string"
        new_dim.documentation = tok[1]
        tok = stack.pop()

    if tok[0] == TokenType.RIGHT_PARENTHESES:
        new_dim.dimension[new_dim.name] = 1
        parser.scope.dimensions[new_dim.name] = new_dim
    else:
        assert tok[0] == TokenType.ASSIGNMENT_ATTRIBUTE,\
               "Invalid dimension expression"
        dimension_expression = get_next_parentheses_unit(stack)
        new_dim.dimension = parse_dimension_expression(
                                parser,
                                dimension_expression
                            )[1]

        # We do a little clean-up
        for name, value in new_dim.dimension.items():
            if value == 0:
                del new_dim.dimension[name]

        # Ensure each dimension is only defined once.
        for old_dim_name, old_dim in parser.scope.dimensions.items():
            all_equal = True
            for item_name, number in new_dim.dimension.items():
                if item_name not in old_dim.dimension or\
                   number != old_dim.dimension[item_name]:
                    all_equal = False
                    break
            if all_equal:
                raise Exception(f"Dimension {old_dim_name} defined twice! " +
                                "Second: {new_dim.name}")

        # Add the dimension to the parser.
        parser.scope.dimensions[new_dim.name] = new_dim


def parse_dimension_expression(parser, stack):
    """
    This function takes an entire dimension expression
    and parses it to a dimension object
    """
    working_stack = list()
    paren_count = 0

    def identifier_to_dimension(id):
        assert id[0] == TokenType.IDENTIFIER, "Invalid dimension given"
        assert id[1] in parser.scope.dimensions,\
            "Undefined dimension in dimension definision"
        # dim_value = dict()
        # dim_value[id[1]] = 1
        return (TokenType.DIMENSION_VALUE, parser.scope.dimensions[id[1]]
                                                 .dimension.copy())

    print(list(map(lambda x: x[0], stack)))

    while len(stack) > 0:
        tok = stack.pop()
        if tok[0] == TokenType.LEFT_PARENTHESES:
            # Increase the parentheses count.
            # If this count is lopsided after a parenthesis
            # collapse, we still need to parse more.
            paren_count += 1
            working_stack.append(tok)
        elif tok[0] == TokenType.RIGHT_PARENTHESES:
            # Decrease the parentheses count
            # for the same reason as above.
            paren_count -= 1

            # Pull all the arguments for this call off the stack.
            args = list()
            while working_stack[-1][0] != TokenType.LEFT_PARENTHESES:
                args.append(working_stack.pop())
            working_stack.pop()

            # Clear the parenthesis off the stack.
            operator = args.pop()

            # Clean the argument list
            for i, arg in enumerate(args):
                # I had a check to do something with parentheses before,
                # but I currently can't think of any reason they would be
                # there, so I'm putting this here for now.
                assert arg[0] != TokenType.LEFT_PARENTHESES and\
                       arg[0] != TokenType.RIGHT_PARENTHESES,\
                       "Invalid token in dimension arg list"

                # Replace all identifiers with a dimension.
                if arg[0] == TokenType.IDENTIFIER:
                    args[i] = identifier_to_dimension(arg)

            # Reverse the args so they're in the expected order
            args.reverse()

            # At this point we have our list of arguments and
            # the operator we'll be using.

            if operator[0] == TokenType.STAR:
                # For the star operation, we add all the values
                # of the dimension expressions together.
                # There can be any number of args.
                operator = args.pop(0)
                for arg in args:
                    for name, value in arg[1].items():
                        if name in operator[1]:
                            operator[1][name] += value
                        else:
                            operator[1][name] = value

            elif operator[0] == TokenType.DIVIDE:
                # For the divide operation, we substract the second
                # argument's values from the first.
                # There should only be two arguments.
                assert len(args) == 2, "Two args required in divide"

                operator = args.pop(0)
                subtrahend = args.pop()

                for name, value in subtrahend[1].items():
                    if name in operator[1]:
                        operator[1][name] -= value
                    else:
                        operator[1][name] = -1 * value

            elif operator[0] == TokenType.EXPT:
                # For the exponent operation, we should multiply
                # all dimensions in the first arguement by the value
                # of the second arguement.
                assert len(args) == 2, "Two args required in exponent"

                # TODO: add check for valid number.
                operator = args.pop(0)
                multiplier = args.pop()

                for name, value in operator[1].items():
                    operator[1][name] = operator[1][name] * multiplier[1]
            else:
                raise Exception("Invalid dimension expression")

            working_stack.append(operator)

            if paren_count == 0:
                return working_stack.pop()
        else:
            # Any tokens that are not parentheses are just data
            # that will be used in a future collapse.
            working_stack.append(tok)

    return working_stack.pop()
