from cmllexer import *
from typing import Dict, Callable, List, Tuple
from lisp_functions import *
from lclasses import *
from ldefun import lisp_defun
from lcond import lisp_cond
from lif import lisp_if
from lwhen import lisp_when

class Parser:
    def __init__(self):
        self.lexer: Lexer = Lexer()


class LispParser(Parser):

    def __init__(self):
        Parser.__init__(self)
        self.lexer = LispLexer()
        self.set_input("")


    def set_input(self, input: str):
        self.scope = Scope(None)
        self.scope.functions["+"] = lisp_add
        self.scope.functions["-"] = lisp_sub
        self.scope.functions["*"] = lisp_mult
        self.scope.functions["/"] = lisp_div
        self.scope.functions["//"] = lisp_divi
        self.scope.functions["mod"] = lisp_mod
        self.scope.functions["rem"] = lisp_mod
        self.scope.functions["print"] = lisp_print
        self.scope.functions["cons"] = lisp_cons
        self.scope.functions["car"] = lisp_car
        self.scope.functions["cdr"] = lisp_cdr
        self.scope.functions["reverse"] = lisp_reverse
        self.scope.functions["list"] = lisp_list
        self.scope.functions["append"] = lisp_append
        self.scope.functions["last"] = lisp_last
        self.scope.functions["="] = lisp_equal
        self.scope.functions["/="] = lisp_neq
        self.scope.functions[">"] = lisp_greaterthan
        self.scope.functions["<"] = lisp_lessthan
        self.scope.functions[">="] = lisp_greaterorequal
        self.scope.functions["<="] = lisp_lessthanorequal
        self.scope.functions["max"] = lisp_max
        self.scope.functions["min"] = lisp_min
        self.scope.functions["and"] = lisp_and
        self.scope.functions["or"] = lisp_or
        self.scope.functions["not"] = lisp_not
        self.scope.functions["logand"] = lisp_logand
        self.scope.functions["logior"] = lisp_logior
        self.scope.functions["logxor"] = lisp_logxor
        self.scope.functions["lognor"] = lisp_lognor
        self.scope.functions["logeqv"] = lisp_logeqv
        self.scope.functions["member"] = lisp_member
        self.scope.functions["defconstant"] = lisp_defconstant

        self.lexer.set_input(input)
    
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
                case TokenType.NIL:
                    self.scope.stack.append((TokenType.NIL, None))
                case TokenType.LEFT_PARENTHESES:
                    self.scope.stack.append((TokenType.LEFT_PARENTHESES, None))
                    self.scope.parentheses_count += 1
                case TokenType.IDENTIFIER:
                    self.scope.stack.append((TokenType.IDENTIFIER, tok[1]))
                    if tok[1] == "defun":
                        lisp_defun(self, input)
                    elif tok[1] == "cond":
                        lisp_cond(self, input)
                    elif tok[1] == "if":
                        lisp_if(self, input)
                    elif tok[1] == "when":
                        lisp_when(self, input)

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

                    if self.scope.func_exists(func_name[1]):

                        ret_val = self.scope.call_func(func_name[1], args)

                        if ret_val is not None:
                            self.scope.stack.append(ret_val)
                    elif func_name[0] == TokenType.IDENTIFIER:
                        raise Exception(f"Invalid function call '{func_name[1]}'")
                    else:
                        self.scope.stack.append(func_name)

                case _:
                    raise Exception("Unknown token type.")
            
            if len(self.scope.stack) > 0 and self.scope.constant_exists(self.scope.stack[-1][1]):
                self.scope.stack.append(self.scope.get_constant(self.scope.stack.pop()[1]))

            if len(input) == 0:
                break
            else:
                tok = input.pop()
        
        assert self.scope.parentheses_count == 0, "Incomplete ending parentheses!"
        

    def parse_input(self, input: str):
        self.add_input(input)
        self.parse()
        if len(self.scope.stack) > 0:
            args = list()
            args.append(self.scope.stack.pop())
            lisp_print("print", args, self.scope)
    
    def recover(self):
        self.lexer.set_input("")
        self.scope.stack.clear()
