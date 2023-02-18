from tokens import *
from lclasses import *
from lhelpers import grab_lisp_statement, run_lisp_stack

def lisp_if(parser, stack):
    parser.scope.stack.pop()
    parser.scope.stack.pop()
    parser.scope.parentheses_count -= 1
    paren_count = 1
    def_stack = list()
    while paren_count > 0:
        assert len(stack) > 0, "Missing close at end of if statement"
        def_stack.append(stack.pop())
        if def_stack[-1][0] == TokenType.LEFT_PARENTHESES:
            paren_count += 1
        elif def_stack[-1][0] == TokenType.RIGHT_PARENTHESES:
            paren_count -= 1
    def_stack.pop()
    def_stack.reverse()

    condition_result = (TokenType.NIL, None)

    if def_stack[-1][0] == TokenType.LEFT_PARENTHESES:
        test_code = grab_lisp_statement(def_stack, keep_parentheses=True)
        condition_result = run_lisp_stack(test_code, parser).pop()
    else:
        condition_result = def_stack.pop()

    if condition_result[0] == TokenType.NIL:
        if def_stack[-1][1] == "then":
            def_stack.pop()
        grab_lisp_statement(def_stack)
        condition_result = run_lisp_stack(def_stack, parser)
        if len(condition_result) > 0:
            parser.scope.stack.append(condition_result.pop())
            return
    else:
        if def_stack[-1][1] == "then":
            def_stack.pop()
        if def_stack[-1][0] == TokenType.LEFT_PARENTHESES:
            run_code = grab_lisp_statement(def_stack, keep_parentheses=True)
            condition_result = run_lisp_stack(run_code, parser)
            if len(condition_result) > 0:
                parser.scope.stack.append(condition_result.pop())
                return
        else:
            parser.scope.stack.append(def_stack.pop())
            return
    
    parser.scope.stack.append((TokenType.NIL, None))
