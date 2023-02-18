from lparser import LispParser

parser = LispParser()



while True:
    test = input(">> ")
    if test == "exit":
        break
    try:
        parser.parse_input(test)
    except Exception as e:
        print(e)
        parser.recover()