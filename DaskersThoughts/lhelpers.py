from cmltokens import *

def grab_lisp_statement(stack, keep_parentheses = False, error_message = "Missing closing parentheses"):

    paren_count = 1
    
    ret_val = list()

    if not keep_parentheses:
        stack.pop()
    else:
        ret_val.append(stack.pop())
    
    
    while paren_count > 0:
        assert len(stack) > 0, error_message
        ret_val.append(stack.pop())
        if ret_val[-1][0] == TokenType.LEFT_PARENTHESES:
            paren_count += 1
        elif ret_val[-1][0] == TokenType.RIGHT_PARENTHESES:
            paren_count -= 1
    
    if not keep_parentheses:
        ret_val.pop()

    ret_val.reverse()

    return ret_val

def run_lisp_stack(stack, parser):
    from lparser import LispParser
    par = LispParser()
    par.scope.parent = parser.scope
    par.parse_stack(stack)
    return par.scope.stack

def evaluate_lisp_stack(stack, parser):
    res_stack = run_lisp_stack(stack, parser)
    if len(res_stack) > 0:
        return res_stack.pop()
    else:
        return (TokenType.NIL, None)

def get_next_stack_value(stack, parser):
    if stack[-1][0] == TokenType.LEFT_PARENTHESES:
        return evaluate_lisp_stack(grab_lisp_statement(stack, keep_parentheses=True), parser)
    else:
        return stack.pop()