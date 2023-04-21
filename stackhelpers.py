from cmltokens import TokenType
from lispclasses import Cons

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
    elif stack[-1][0] == TokenType.QUOTE:
        print("TODO")
        raise Exception("TODO")
    else:
        return stack.pop()


def get_lisp_quoted_list(stack):
    """
    Returns a cons of the rest of list.
    The first element on the stack should
    be the the element after the opening parenthesis.
    """
    ret_val = Cons()
    ret_val.first = stack.pop()
    if ret_val.first[0] == TokenType.LEFT_PARENTHESES:
        ret_val.first = get_lisp_quoted_list(stack)
    if ret_val.first[0] == TokenType.RIGHT_PARENTHESES:
        return (TokenType.NIL, None)
    ret_val.second = get_lisp_quoted_list(stack)
    return (TokenType.CONS, ret_val)

def lisp_to_string(stack):
    output = ""
    while len(stack) > 0:
        tok = stack.pop()
        if tok[0] == TokenType.LEFT_PARENTHESES:
            output += " ("
        elif tok[0] == TokenType.RIGHT_PARENTHESES:
            output += ") "
        elif tok[0] == TokenType.STRING:
            output += f' "{tok[1]}"'
        elif tok[0] == TokenType.IDENTIFIER:
            output += f' {tok[1]}'
        else:
            raise Exception(f"Unknown token type {tok[0]}")