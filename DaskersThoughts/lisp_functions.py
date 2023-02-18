
from typing import List, Tuple
from lclasses import *

def lisp_add(name: any, args: List[Tuple[str, any]], scope):
        args.reverse()
        result = args.pop()
        assert result[0] == TokenType.NUMBER

        while len(args) > 0:
            next = args.pop()
            assert next[0] == TokenType.NUMBER
            result = (TokenType.NUMBER, result[1] + next[1])
        return result


def lisp_sub(name: any, args: List[Tuple[str, any]], scope):
        args.reverse()
        result = args.pop()
        assert result[0] == TokenType.NUMBER

        while len(args) > 0:
            next = args.pop()
            assert next[0] == TokenType.NUMBER
            result = (TokenType.NUMBER, result[1] - next[1])
        return result


def lisp_mult(name: any, args: List[Tuple[str, any]], scope):
        args.reverse()
        result = args.pop()
        assert result[0] == TokenType.NUMBER

        while len(args) > 0:
            next = args.pop()
            assert next[0] == TokenType.NUMBER
            result = (TokenType.NUMBER, result[1] * next[1])
        return result

def lisp_div(name: any, args: List[Tuple[str, any]], scope):
        args.reverse()
        result = args.pop()
        assert result[0] == TokenType.NUMBER

        while len(args) > 0:
            next = args.pop()
            assert next[0] == TokenType.NUMBER
            result = (TokenType.NUMBER, result[1] / next[1])
        return result

def lisp_divi(name: any, args: List[Tuple[str, any]], scope):
        args.reverse()
        result = args.pop()
        assert result[0] == TokenType.NUMBER

        while len(args) > 0:
            next = args.pop()
            assert next[0] == TokenType.NUMBER
            result = (TokenType.NUMBER, result[1] // next[1])
        return result

def lisp_mod(name: any, args: List[Tuple[str, any]], scope):
        args.reverse()
        result = args.pop()
        assert result[0] == TokenType.NUMBER

        while len(args) > 0:
            next = args.pop()
            assert next[0] == TokenType.NUMBER
            result = (TokenType.NUMBER, result[1] % next[1])
        return result

def lisp_cons(name: any, args: List[Tuple[str, any]], scope):
    assert len(args) == 2, "Too many args for cons"
    ret_val = list()
    ret_val.append(args[0])
    ret_val.append(args[1])
    return (TokenType.CONS, ret_val)

def lisp_car(name: any, args: List[Tuple[str, any]], scope):
    assert len(args) == 1, "Too many args for cons"
    ret_val = args[0][1][0]
    return ret_val

def lisp_cdr(name: any, args: List[Tuple[str, any]], scope):
    assert len(args) == 1, "One arg needed for cons"
    ret_val = args[0][1][1]
    return ret_val

def lisp_reverse(name: any, args: List[Tuple[str, any]], scope):
    assert len(args) == 1, "One arg needed for reverse"
    old_cons = args[0]

    new_cons = (TokenType.NIL, None)

    while old_cons[0] != TokenType.NIL:
        tmp = list()
        tmp.append(old_cons[1][0])
        tmp.append(new_cons)
        new_cons = (TokenType.CONS, tmp)
        old_cons = old_cons[1][1]
    
    return new_cons

def lisp_list(name: any, args: List[Tuple[str, any]], scope):
    assert len(args) > 0, "At least one arg needed for list"

    new_list = (TokenType.NIL, None)

    while len(args) > 0 != TokenType.NIL:
        tmp = list()
        tmp.append(args.pop())
        tmp.append(new_list)
        new_list = (TokenType.CONS, tmp)
    
    return new_list

def lisp_append(name: any, args: List[Tuple[str, any]], scope):
    assert len(args) > 1, "At least two args needed for append"
    
    first_list = list()

    old_cons = args[0]
    while old_cons[0] != TokenType.NIL:
        assert old_cons[0] == TokenType.CONS, "Not a valid list in append"
        first_list.append(old_cons[1][0])
        old_cons = old_cons[1][1]
    
    new_list = args[1]

    while len(first_list) > 0:
        tmp = list()
        tmp.append(first_list.pop())
        tmp.append(new_list)
        new_list = (TokenType.CONS, tmp)
    
    if len(args) > 2:
        new_args = list()
        new_args.append(new_list)
        new_args += args[2:]
        return lisp_append(name, new_args, scope)

    return new_list

def lisp_last(name: any, args: List[Tuple[str, any]], scope):
    assert len(args) == 1, "Only one list needed for last"
    
    if args[0][0] == TokenType.NIL:
        return args[0]

    first_list = list()

    old_cons = args[0]
    while old_cons[0] != TokenType.NIL:
        assert old_cons[0] == TokenType.CONS, "Not a valid list in append"
        first_list.append(old_cons[1][0])
        old_cons = old_cons[1][1]
    
    new_list = list()
    new_list.append(first_list.pop())
    new_list.append((TokenType.NIL, None))
    return (TokenType.CONS, new_list)

def lisp_equal(name: any, args: List[Tuple[str, any]], scope):
    assert len(args) > 1, "Two args needed for equal comparison"

    if args[0][0] != args[1][0]:
        return (TokenType.NIL, None)
    
    if args[0][0] == TokenType.CONS:
        new_args = list()
        new_args.append(args[0][1][0])
        new_args.append(args[1][1][0])
        if lisp_equal(name, new_args, scope)[0] == TokenType.NIL:
            return (TokenType.NIL, None)
        else:
            new_args = list()
            new_args.append(args[0][1][1])
            new_args.append(args[1][1][1])
            return lisp_equal(name, new_args, scope)
    else:
        if args[0][1] == args[1][1]:
            return (TokenType.TRUE, None)
        else:
            return (TokenType.NIL, None)

def lisp_member(name: any, args: List[Tuple[str, any]], scope):
    assert len(args) == 2, "Two args needed for member"
    if args[1][0] == TokenType.NIL:
        return args[1]
    
    assert args[1][0] == TokenType.CONS, "Second arg of member must be a list"

    ret_val = args[1]
    while ret_val[0] != TokenType.NIL:
        new_args = list()
        new_args.append(args[0])
        new_args.append(ret_val[1][0])
        result = lisp_equal("=", new_args, scope)
        if result[0] == TokenType.TRUE:
            break
        else:
            ret_val = ret_val[1][1]


    return ret_val
    


def lisp_cons_to_str(cons, in_list = False):
    if not in_list:
        return f"({lisp_cons_to_str(cons, in_list=True)})"

    if cons[1][0] != TokenType.NIL and cons[1][0] != TokenType.CONS and cons[0][0] != TokenType.CONS:
        return f"{lisp_atom_to_str(cons[0])} . {lisp_atom_to_str(cons[1])}"
    
    elif cons[1][0] != TokenType.NIL and cons[1][0] != TokenType.CONS and cons[0][0] == TokenType.CONS:
        return f"{lisp_atom_to_str(cons[0])} . {lisp_atom_to_str(cons[1])}"

    elif cons[0][0] != TokenType.CONS and cons[1][0] == TokenType.NIL:
        return f"{lisp_atom_to_str(cons[0])}"

    elif cons[0][0] == TokenType.CONS and cons[1][0] == TokenType.CONS:
        return f"({lisp_cons_to_str(cons[0][1], in_list=True)}) {lisp_cons_to_str(cons[1][1], in_list=True)}"
    
    elif cons[0][0] != TokenType.CONS and cons[1][0] == TokenType.CONS:
        return f"{lisp_atom_to_str(cons[0])} {lisp_cons_to_str(cons[1][1], in_list=True)}"

def lisp_atom_to_str(atom):
    match atom[0]:
        case TokenType.NUMBER:
            return str(atom[1])
        case TokenType.STRING:
            return str(atom[1])
        case TokenType.CONS:
            return lisp_cons_to_str(atom[1])
        case TokenType.NIL:
            return "NIL"
        case TokenType.TRUE:
            return "TRUE"
        case _:
            raise Exception("Unsupported type")

def lisp_print(name: any, args: List[Tuple[str, any]], scope):
    assert len(args) > 0, "Too few args for print"

    print(lisp_atom_to_str(args[0]))

    return (TokenType.NIL, None)

def lisp_defconstant(name: any, args: List[Tuple[str, any]], scope):
    assert len(args) == 2, "Two args for defconstant"

    scope.add_constant(args[0][1], args[1])

def lisp_neq(name: any, args: List[Tuple[str, any]], scope):
    assert len(args) > 1, "Comparison requires at least 2 args"

    for i in range(len(args)):
        for j in range(len(args)):
            if i == j:
                continue
            else:
                new_args = list()
                new_args.append(args[i])
                new_args.append(args[j])
                if lisp_equal("=", new_args, scope):
                    return (TokenType.NIL, None)
    
    return (TokenType.TRUE, None)

def lisp_greaterthan(name: any, args: List[Tuple[str, any]], scope):
    assert len(args) > 1, "Comparison requires at least 2 args"

    for i in range(len(args) - 1):
        if args[i][1] <= args[i + 1][1]:
            return (TokenType.NIL, None)

    return (TokenType.TRUE, None)

def lisp_lessthan(name: any, args: List[Tuple[str, any]], scope):
    assert len(args) > 1, "Comparison requires at least 2 args"

    for i in range(len(args) - 1):
        if args[i][1] >= args[i + 1][1]:
            return (TokenType.NIL, None)

    return (TokenType.TRUE, None)

def lisp_greaterorequal(name: any, args: List[Tuple[str, any]], scope):
    assert len(args) > 1, "Comparison requires at least 2 args"

    for i in range(len(args) - 1):
        if args[i][1] < args[i + 1][1]:
            return (TokenType.NIL, None)

    return (TokenType.TRUE, None)

def lisp_lessthanorequal(name: any, args: List[Tuple[str, any]], scope):
    assert len(args) > 1, "Comparison requires at least 2 args"

    for i in range(len(args) - 1):
        if args[i][1] > args[i + 1][1]:
            return (TokenType.NIL, None)

    return (TokenType.TRUE, None)

def lisp_max(name: any, args: List[Tuple[str, any]], scope):
    assert len(args) > 1, "Comparison requires at least 2 args"

    ret_result = args[0]

    for i in range(1, len(args)):
        if ret_result[1] < args[i][1]:
            ret_result = args[i]

    return ret_result

def lisp_min(name: any, args: List[Tuple[str, any]], scope):
    assert len(args) > 1, "Comparison requires at least 2 args"

    ret_result = args[0]

    for i in range(1, len(args)):
        if ret_result[1] > args[i][1]:
            ret_result = args[i]

    return ret_result

def lisp_and(name: any, args: List[Tuple[str, any]], scope):
    assert len(args) > 1, "Comparison requires at least 2 args"

    for i in range(len(args)):
        if args[i][0] == TokenType.NIL:
            return args[i]
    
    return args[-1]

def lisp_or(name: any, args: List[Tuple[str, any]], scope):
    assert len(args) > 1, "Comparison requires at least 2 args"

    for i in range(len(args)):
        if args[i][0] != TokenType.NIL:
            return args[i]
    
    return (TokenType.NIL, None)

def lisp_not(name: any, args: List[Tuple[str, any]], scope):
    assert len(args) == 1, "Not requires 1 arg"

    if args[0][0] == TokenType.NIL:
        return (TokenType.TRUE, None)
    else:
        return (TokenType.NIL, None)

def lisp_logand(name: any, args: List[Tuple[str, any]], scope):

    ret_val = -1

    for i in range(len(args)):
        assert args[i][0] == TokenType.NUMBER
        ret_val &= args[i][1]
    
    return (TokenType.NUMBER, ret_val)

def lisp_logior(name: any, args: List[Tuple[str, any]], scope):

    ret_val = 0

    for i in range(len(args)):
        assert args[i][0] == TokenType.NUMBER
        ret_val |= args[i][1]
    
    return (TokenType.NUMBER, ret_val)

def lisp_logxor(name: any, args: List[Tuple[str, any]], scope):

    ret_val = 0

    for i in range(len(args)):
        assert args[i][0] == TokenType.NUMBER
        ret_val ^= args[i][1]
    
    return (TokenType.NUMBER, ret_val)

def lisp_lognor(name: any, args: List[Tuple[str, any]], scope):

    ret_val = -1

    for i in range(len(args)):
        assert args[i][0] == TokenType.NUMBER
        ret_val = (ret_val | args[i][1]) ^ -1
    
    return (TokenType.NUMBER, ret_val)

def lisp_logeqv(name: any, args: List[Tuple[str, any]], scope):

    ret_val = -1

    for i in range(len(args)):
        assert args[i][0] == TokenType.NUMBER
        ret_val = (ret_val ^ args[i][1]) ^ -1
    
    return (TokenType.NUMBER, ret_val)

#def create_func(name: any, args: List[Tuple[str, any]], scope)