from stackhelpers import get_next_parentheses_unit
from cmlclasses import Unit, ModelValue
from cmlparser import CMLParser
from typing import List, Tuple
from cmltokens import TokenType
from cmlmath import parse_math_expression


def parse_constantquantity(parser: CMLParser, args: List[Tuple[TokenType, any]]):
    """
    [summary]

    Parses a args containing a Constant Quantity description.

    The args will come in without the first parentheses or defConstantQuantity.

    ### Parameters
    1. parser: CMLParser
    - The cml parser we are using.
    2. args: List[Tuple[TokenType, any]]
    - The args to parse the unit from.

    """

    tok = args.pop()
    assert tok[0] == TokenType.IDENTIFIER, "Constant Quantity given without a name"
    new_constant_quantity = Unit(tok[1])
    assert new_constant_quantity.name not in parser.scope.units(),\
        f"Dimension {new_constant_quantity.name} already exists"
    
    quantity_assigned = False

    while len(args) > 0:

        tok = args.pop()

        if tok[0] == TokenType.IDENTIFIER:

            if tok[0] == ":DIMENSION":
                tok = args.pop()
                assert tok[1] in parser.scope.dimensions(),\
                    "Dimension supplied does not exist"
                new_unit_value = ModelValue()
                new_unit_value.dimension = parser.scope.get_dimension(tok[1])\
                                                 .dimension.copy()
                new_unit_value.quantity = 1

                if len(new_constant_quantity.value.dimension) == 0 and\
                   new_constant_quantity.value.quantity == 0:
                    new_constant_quantity.value = new_unit_value
                    new_constant_quantity.base_unit = True
            elif tok[1] == ":=":
                unit_expression = get_next_parentheses_unit(args)
                unit_expression.reverse()
                unit_value = parse_math_expression(parser, unit_expression)
                assert unit_value[0] == TokenType.MODEL_VALUE,\
                    "Result of unit expression should be a value."
                new_constant_quantity.value = unit_value[1]
                assert new_constant_quantity.value.dimension is not None,\
                    f"Invalid quantity expression for {new_constant_quantity.name}"
                new_constant_quantity.base_unit = False
                quantity_assigned = True
            else:
                property_name = tok[1]
                new_constant_quantity.addons[property_name] = get_next_parentheses_unit(args)
        else:
            raise Exception(f"Invalid unit definition for {new_constant_quantity.name}")

    assert quantity_assigned, f"Assignment required in constant definition for {new_constant_quantity.name}"

    # Add the dimension to the parser.
    parser.scope.add_unit(new_constant_quantity)