
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

#def lisp_cons()

#def create_func(name: any, args: List[Tuple[str, any]], scope)