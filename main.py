import cmlparser
import sys

input_text = open("CML/heater.cml").read()
parser = cmlparser.CMLParser()
parser.reset()
parser.parse_string(input_text)

# x = list(map(lambda x: x.dimension, list(parser.scope.dimensions.values())))
x = list(map(lambda x: x.name, list(parser.scope.modelfragments().values())))

print(x)
