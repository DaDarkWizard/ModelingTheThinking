from lparser import LispParser

ti = LispParser()

ti.parse_input("(= 3 3)")
ti.parse_input("(dfsg 3 (list 1 3 54))")