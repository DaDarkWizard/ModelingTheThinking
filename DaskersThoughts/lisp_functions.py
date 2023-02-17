
from typing import List, Tuple

def lisp_add(args: List[Tuple[str, any]], scope):
        args.reverse()
        result = args.pop()
        assert result[0] == "NUMBER"

        while len(args) > 0:
            next = args.pop()
            assert next[0] == "NUMBER"
            result = ("NUMBER", result[1] + next[1])
        return result


def lisp_sub(args: List[Tuple[str, any]], scope):
        args.reverse()
        result = args.pop()
        assert result[0] == "NUMBER"

        while len(args) > 0:
            next = args.pop()
            assert next[0] == "NUMBER"
            result = ("NUMBER", result[1] - next[1])
        return result


def lisp_mult(args: List[Tuple[str, any]], scope):
        args.reverse()
        result = args.pop()
        assert result[0] == "NUMBER"

        while len(args) > 0:
            next = args.pop()
            assert next[0] == "NUMBER"
            result = ("NUMBER", result[1] * next[1])
        return result

def lisp_div(args: List[Tuple[str, any]], scope):
        args.reverse()
        result = args.pop()
        assert result[0] == "NUMBER"

        while len(args) > 0:
            next = args.pop()
            assert next[0] == "NUMBER"
            result = ("NUMBER", result[1] / next[1])
        return result

def lisp_divi(args: List[Tuple[str, any]], scope):
        args.reverse()
        result = args.pop()
        assert result[0] == "NUMBER"

        while len(args) > 0:
            next = args.pop()
            assert next[0] == "NUMBER"
            result = ("NUMBER", result[1] // next[1])
        return result

def lisp_mod(args: List[Tuple[str, any]], scope):
        args.reverse()
        result = args.pop()
        assert result[0] == "NUMBER"

        while len(args) > 0:
            next = args.pop()
            assert next[0] == "NUMBER"
            result = ("NUMBER", result[1] % next[1])
        return result