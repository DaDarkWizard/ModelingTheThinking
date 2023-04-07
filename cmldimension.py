from typing import Dict, List, Tuple
from stackhelpers import TokenType, get_next_parentheses_unit
from cmlclasses import Dimension
import cmlparser


def parse_dimension(parser: cmlparser.CMLParser, args):
    """[summary]

        Parses a args containing a dimension description.

        The args will come in without the first parentheses or def-dimension.

        ### Parameters
        1. parser: CMLParser
           - The cml parser we are using.
        2. args: List[Tuple[TokenType, any]]
           - The args to parse the dimension from.
    """

    tok = args.pop()
    assert tok[0] == TokenType.IDENTIFIER, "Dimension given without a name"
    new_dim = Dimension(tok[1])
    assert new_dim.name not in parser.scope.dimensions(),\
           f"Dimension {new_dim.name} already exists"

    while len(args) > 0:

        tok = args.pop()

        if tok[0] == TokenType.IDENTIFIER:
            if tok[1] == ":DOCUMENTATION":
                tok = args.pop()
                assert tok[0] == TokenType.STRING,\
                    "Documentation attribute given without string"
                new_dim.documentation = tok[1]
            elif tok[1] == ":=":
                dimension_expression = get_next_parentheses_unit(args)
                new_dim.dimension = parse_dimension_expression(
                                        parser,
                                        dimension_expression
                                    )[1]

                # We do a little clean-up
                simplify_dimension(new_dim.dimension)

                # Ensure each dimension is only defined once.
                for old_dim_name, old_dim in parser.scope.dimensions().items():
                    all_equal = True
                    for item_name, number in new_dim.dimension.items():
                        if item_name not in old_dim.dimension or\
                        number != old_dim.dimension[item_name]:
                            all_equal = False
                            break
                    if all_equal:
                        raise Exception(f"Dimension {old_dim_name} defined twice! " +
                                        "Second: {new_dim.name}")
            else:
                property_name = tok[1]
                new_dim.addons[property_name] = get_next_parentheses_unit(args)
        else:
            raise Exception(f"Invalid dimension definition for {new_dim.name}")

    # Setup base dimensions
    if len(new_dim.dimension) < 1:
        new_dim.dimension[new_dim.name] = 1

    # Add the dimension to the parser.
    parser.scope.add_dimension(new_dim)


def parse_dimension_expression(parser, stack):
    """
    This function takes an entire dimension expression
    and parses it to a dimension object
    """
    working_stack = list()
    paren_count = 0

    def identifier_to_dimension(id):
        assert id[0] == TokenType.IDENTIFIER, "Invalid dimension given"
        assert id[1] in parser.scope.dimensions(),\
            f"Undefined dimension {id[1]} in dimension definition"
        # dim_value = dict()
        # dim_value[id[1]] = 1
        return (TokenType.DIMENSION_VALUE, parser.scope.get_dimension(id[1])
                                                 .dimension.copy())
    
    if len(stack) == 2:
        if stack[0] == TokenType.IDENTIFIER:
            dim = identifier_to_dimension(stack)
            return dim

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
            assert operator[0] == TokenType.IDENTIFIER,\
                   "Invalid dimension expression."

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

            if operator[1] == "*":
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

            elif operator[1] == "/":
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

            elif operator[1] == "EXPT":
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


def simplify_dimension(dim: Dict[str, int]):
    """
    Simplifies a dimension dictionary (removes 0s)
    """
    for name, value in dim.items():
        if value == 0:
            del dim[name]
    return dim


def dim_equal(a: Dict[str, int], b: Dict[str, int]):
    """
    Compares if two dimensions are equal.
    """
    simplify_dimension(a)
    simplify_dimension(b)
    for k in a.keys():
        if k not in b:
            return False
        if a[k] != b[k]:
            return False
    for k in b.keys():
        if k not in a:
            return False
    return True


def dim_div(a: Dict[str, int], b: Dict[str, int]):
    """
    Divides the first dimension by the second.
    """
    result = a.copy()
    for k, v in b:
        if k not in result:
            result[k] = -1 * v
        else:
            result[k] -= v
    return simplify_dimension(result)


def dim_mul(a: Dict[str, int], b: Dict[str, int]):
    """
    Multiplies the first dimension by the second.
    """
    result = a.copy()
    for k, v in b.items():
        if k not in result:
            result[k] = v
        else:
            result[k] += v
    return simplify_dimension(result)
