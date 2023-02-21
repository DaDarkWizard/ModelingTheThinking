from cmltokens import *
from lclasses import *
from lhelpers import grab_lisp_statement, run_lisp_stack, evaluate_lisp_stack, get_next_stack_value
from lisp_functions import lisp_equal

def lisp_case(parser, stack):
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

    test_result = get_next_stack_value(def_stack, parser)

    while len(def_stack) > 0:
        test_case = grab_lisp_statement(def_stack, error_message="Malformed cond")

        cur_case = get_next_stack_value(test_case, parser)

        eq_args = list()
        eq_args.append(test_result)
        eq_args.append(cur_case)

        if lisp_equal("=", eq_args, parser.scope)[0] != TokenType.NIL:
            parser.scope.stack.append(get_next_stack_value(test_case, parser))
            return
    
    parser.scope.stack.append((TokenType.NIL, None))