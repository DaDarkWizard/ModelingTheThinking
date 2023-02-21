from tokens import *
from lclasses import *
from lhelpers import grab_lisp_statement, run_lisp_stack

def lisp_cond(parser, stack):
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

    while len(def_stack) > 0:
        test_action = grab_lisp_statement(def_stack, error_message="Malformed cond")

        test_code = grab_lisp_statement(test_action, keep_parentheses=True, error_message="Malformed cond")

        test_result = (TokenType.NIL, None)
        if test_code[-1][0] == TokenType.LEFT_PARENTHESES:
            test_result = run_lisp_stack(test_code, parser).pop()
        else:
            test_result = test_code.pop()

        if test_result[0] == TokenType.NIL:
            continue
        else:
            if test_action[-1] == TokenType.LEFT_PARENTHESES:
                action_result = run_lisp_stack(test_action, parser)
                if len(action_result) > 1:
                    parser.scope.stack.append(action_result.pop())
                return
            else:
                parser.scope.stack.append(test_action.pop())
                return
    
    parser.scope.stack.append((TokenType.NIL, None))
