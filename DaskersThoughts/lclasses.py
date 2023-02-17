from typing import Dict, Callable, List, Tuple
from tokens import *

class Scope:
    def __init__(self, parent = None):
        self.parent = parent
        self.functions : Dict[any, Callable[[List[Tuple[str, any]], Scope], Tuple[str, any]]] = dict()
        self.stack: List[Tuple[str, any]] = list()
        self.parentheses_count = 0
        self.defer_execution = False
        self.defer_parentheses_count = 0
        
    def call_func(self, name: any, args: List[Tuple[str, any]]):
        if name in self.functions:
            return self.functions[name](name, args, self)
        elif isinstance(self.parent, Scope):
            ret_val: Tuple[str, any] = self.parent.call_func(name, args)
            return ret_val
        else:
            return None
    
    def func_exists(self, name: any):
        if name in self.functions:
            return True
        elif isinstance(self.parent, Scope):
            ret_val: bool = self.parent.func_exists()
            return ret_val
        else:
            return False
    
    def add_func(self, func):
        self.functions[func.name] = func.call_function

class LispFunction:
    def __init__(self, name:any, args: list, stack: list):
        self.name = name
        self.args = args
        self.stack = stack
        self.doc_comment = ""
        if len(self.stack) > 0 and self.stack[-1][0] == TokenType.STRING:
            self.doc_comment = self.stack.pop()

    def call_function(self, name: str, args: list, scope: Scope):
        assert len(args) == len(self.args)

        from lparser import LispParser
        working_stack = self.stack.copy()

        for i in range(len(args)):
            for j in range(len(working_stack)):
                if working_stack[j][1] == self.args[i]:
                    working_stack[j] = args[i]
        
        par = LispParser()
        new_scope = Scope(scope)
        par.scope = new_scope
        par.parse_stack(working_stack)
        if len(par.scope.stack) > 0:
            return par.scope.stack[-1]
        
