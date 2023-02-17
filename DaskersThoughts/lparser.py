from llexer import *
from typing import Dict, Callable, List, Tuple
from lisp_functions import *
from lclasses import *

class Parser:
    def __init__(self):
        self.lexer: Lexer = Lexer()


class LispParser(Parser):

    def __init__(self):
        Parser.__init__(self)
        self.lexer = LispLexer()
        self.set_input("")


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
        toks = self.lexer.lex_all()

        toks.reverse()

        self.parse_stack(toks)

        
    
    def parse_stack(self, input: list):
        tok = input.pop()

        while True:
            match tok[0]:
                case TokenType.STRING:
                    self.scope.stack.append((TokenType.STRING, tok[1]))
                case TokenType.NUMBER:
                    self.scope.stack.append((TokenType.NUMBER, tok[1]))
                case TokenType.INTEGER:
                    self.scope.stack.append((TokenType.NUMBER, tok[1]))
                case TokenType.FLOAT:
                    self.scope.stack.append((TokenType.NUMBER, tok[1]))
                case TokenType.LEFT_PARENTHESES:
                    self.scope.stack.append((TokenType.LEFT_PARENTHESES, None))
                    self.scope.parentheses_count += 1
                case TokenType.IDENTIFIER:
                    self.scope.stack.append((TokenType.IDENTIFIER, tok[1]))
                    if tok[1] == "defun":
                        self.scope.stack.pop()
                        self.scope.stack.pop()
                        self.scope.parentheses_count -= 1
                        paren_count = 1
                        def_stack = list()
                        while paren_count > 0:
                            assert len(input) > 0, "Missing close at end of function definition"
                            def_stack.append(input.pop())
                            if def_stack[-1][0] == TokenType.LEFT_PARENTHESES:
                                paren_count += 1
                            elif def_stack[-1][0] == TokenType.RIGHT_PARENTHESES:
                                paren_count -= 1
                        def_stack.pop()
                        def_stack.reverse()
                        new_func_name = def_stack.pop()
                        assert new_func_name[0] != TokenType.LEFT_PARENTHESES and \
                                new_func_name[0] != TokenType.RIGHT_PARENTHESES, "Invalid function definition."
                        new_func_args = list()
                        assert def_stack.pop()[0] == TokenType.LEFT_PARENTHESES, "Invalid function definition."
                        new_func_args.append(def_stack.pop())
                        while new_func_args[-1][0] != TokenType.RIGHT_PARENTHESES:
                            new_func_args.append(def_stack.pop())
                        new_func_args.pop()
                        new_func_args = list(map(lambda x: x[1], new_func_args))
                        new_func = LispFunction(new_func_name[1], new_func_args, def_stack)
                        self.scope.add_func(new_func)

                case TokenType.RIGHT_PARENTHESES:
                    self.scope.parentheses_count -= 1
                    if self.scope.parentheses_count < 0:
                        raise Exception("Mismatched parentheses!")
                    
                    args: Tuple[str, any] = list()

                    while self.scope.stack[-1][0] != TokenType.LEFT_PARENTHESES:
                        args.append(self.scope.stack.pop())
                    
                    self.scope.stack.pop()

                    func_name = args.pop()

                    args.reverse()

                    ret_val = self.scope.call_func(func_name[1], args)

                    if ret_val is not None:
                        self.scope.stack.append(ret_val)

                case _:
                    raise Exception("Unknown token type.")
            
            if len(input) == 0:
                break
            else:
                tok = input.pop()
        
        assert self.scope.parentheses_count == 0, "Incomplete ending parentheses!"
        

    def parse_input(self, input: str):
        self.add_input(input)
        self.parse()
        if len(self.scope.stack) > 0:
            print(self.scope.stack.pop())
