from llexer import *
from typing import Dict, Callable, List, Tuple
from lisp_functions import *

class Parser:
    def __init__(self):
        self.lexer: Lexer = Lexer()


class Scope:
    def __init__(self, parent = None):
        self.parent = parent
        self.functions : Dict[any, Callable[[List[Tuple[str, any]], Scope], Tuple[str, any]]] = dict()
        self.stack: List[Tuple[str, any]] = list()
        self.parentheses_count = 0
        
    def call_func(self, name: any, args: List[Tuple[str, any]]):
        if name in self.functions:
            return self.functions[name](args, self)
        elif isinstance(self.parent, Scope):
            ret_val: Tuple[str, any] = self.parent.call_func(name, args)
            return ret_val
        else:
            return None


class LispParser(Parser):

    def __init__(self):
        Parser.__init__(self)
        self.lexer = LispLexer()


    def set_input(self, input: str):
        self.lexer.set_input(input)
        self.scope = Scope(None)
        self.scope.functions["+"] = lisp_add
        self.scope.functions["-"] = lisp_sub
        self.scope.functions["*"] = lisp_mult
        self.scope.functions["/"] = lisp_div
        self.scope.functions["//"] = lisp_divi
        self.scope.functions["%"] = lisp_mod
    
    def add_input(self, input: str):
        self.lexer.set_input(input)
    
    def parse(self):
        tok = self.lexer.lex()

        while tok.type != TokenType.END:
            match tok.type:
                case TokenType.STRING:
                    self.scope.stack.append(("STRING", tok.value))
                case TokenType.INTEGER:
                    self.scope.stack.append(("NUMBER", tok.value))
                case TokenType.FLOAT:
                    self.scope.stack.append(("NUMBER", tok.value))
                case TokenType.LEFT_PARENTHESES:
                    self.scope.stack.append(("L_PAREN", None))
                    self.scope.parentheses_count += 1
                case TokenType.IDENTIFIER:
                    self.scope.stack.append(("IDENTIFIER", tok.value))
                case TokenType.RIGHT_PARENTHESES:
                    self.scope.parentheses_count -= 1
                    if self.scope.parentheses_count < 0:
                        raise Exception("Mismatched parentheses!")
                    
                    args: Tuple[str, any] = list()

                    while self.scope.stack[-1][0] != "L_PAREN":
                        args.append(self.scope.stack.pop())
                    
                    self.scope.stack.pop()

                    func_name = args.pop()

                    args.reverse()

                    ret_val = self.scope.call_func(func_name[1], args)

                    self.scope.stack.append(ret_val)

                case _:
                    raise Exception("Unknown token type.")
            
            tok = self.lexer.lex()
        
        print(self.scope.stack)

ti = LispParser()

ti.set_input("(+ (- 6 7) 3)")
ti.parse()