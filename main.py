import cmlparser
import sys

input_text = open("CML/dimensionstest.cml").read()
parser = cmlparser.CMLParser()
parser.reset()
parser.parse_string(input_text)

# x = list(map(lambda x: x.dimension, list(parser.scope.dimensions.values())))
x = list(map(lambda x: x.value.to_string(), list(parser.scope.modelfragments().values())))

print(x)
