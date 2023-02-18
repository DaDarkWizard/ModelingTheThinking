from lparser import LispParser
import traceback

parser = LispParser()



while True:
    test = input(">> ")
    if test == "exit":
        break
    try:
        parser.parse_input(test)
    except Exception as e:
        traceback.print_exc()
        parser.recover()