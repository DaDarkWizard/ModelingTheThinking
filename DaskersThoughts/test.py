from lparser import LispParser

ti = LispParser()

ti.parse_input("(defun add (one two) (+ one two))")
ti.parse_input("(add 4 5)")