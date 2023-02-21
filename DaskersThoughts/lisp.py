from lparser import LispParser
import traceback
import sys

parser = LispParser()

if len(sys.argv) > 1:
    file = open(sys.argv[1])
    input_text = file.read()
    file.close()
    parser.set_input(input_text)
    parser.parse()
else:
    while True:
        test = input(">> ")
        if test == "exit":
            break
        try:
            parser.parse_input(test)
        except Exception as e:
            traceback.print_exc()
            parser.recover()