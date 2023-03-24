from cmltokens import *

def get_rest_of_parentheses(stack):
    paren_count = 1

    ret_val = list()

    while paren_count > 0 and len(stack) > 0:
        tok = stack.pop()
        if tok[0] == TokenType.LEFT_PARENTHESES:
            paren_count += 1
        elif tok[0] == TokenType.RIGHT_PARENTHESES:
            paren_count -= 1
        ret_val.append(tok)

    assert paren_count == 0, "Failed to get ending parentheses"

    ret_val.reverse()

    return ret_val

def get_next_parentheses_unit(stack):
    ret_val = list()
    if stack[-1][0] == TokenType.LEFT_PARENTHESES:
        ret_val.append(stack.pop())
        rest_stack = get_rest_of_parentheses(stack)
        while len(rest_stack) > 0:
            ret_val.append(rest_stack.pop())
        ret_val.reverse()
        return ret_val
    else:
        return stack.pop()
