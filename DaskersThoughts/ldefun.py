from tokens import *
from lclasses import *

def lisp_defun(parser, stack):
    parser.scope.stack.pop()
    parser.scope.stack.pop()
    parser.scope.parentheses_count -= 1
    paren_count = 1
    def_stack = list()
    while paren_count > 0:
        assert len(stack) > 0, "Missing close at end of function definition"
        def_stack.append(stack.pop())
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
    parser.scope.add_func(new_func)
