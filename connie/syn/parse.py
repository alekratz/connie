import functools
from typing import Optional, Sequence
from connie.syn.lex import Lex
from connie.syn.ast import *


class Parse:
    tokens = Lex.tokens

    start = 'body'

    def __init__(self, source: str, source_name: Optional[str]=None) -> None:
        import ply.yacc as yacc
        lexer = Lex(source, source_name)
        self.lexer = lexer
        self.parser = yacc.yacc(module=self)

    @property
    def source_name(self) -> Optional[str]:
        return self.lexer.source_name

    @property
    def source(self) -> str:
        return self.lexer.source

    def p_body(self, p):
        r"""
        body        : atom body
        """
        p[0] = [p[1]] + p[2]

    def p_empty_body(self, p):
        r"""
        body        :
        """
        p[0] = []

    def p_atom(self, p):
        r"""
        atom    : quote
                | value
                | assign
                | list
                | sym
                | ident
        """
        p[0] = p[1]

    def p_ident(self, p):
        r"""
        ident : IDENT
        """
        p[0] = Ident(span = p.linespan(1), name = p[1])

    def p_sym(self, p):
        r"sym   : SYM"
        p[0] = Sym(span = p.linespan(1), sym = p[1])

    def p_list(self, p):
        r"list  : LBRACKET body RBRACKET"
        start, _ = p.linespan(1)
        _, end = p.linespan(3)
        p[0] = List(span = (start, end), body = p[2])

    def p_assign(self, p):
        r"assign : SET"
        p[0] = Assign(span = p.linespan(1), name = p[1][1:])

    def p_quote(self, p):
        r"quote : LBRACE body RBRACE"
        start, _ = p.linespan(1)
        _, end = p.linespan(3)
        p[0] = Quote(span = (start, end), body = p[2])

    def p_str_value(self, p):
        r"""
        value   : STR_LIT
        """
        p[0] = StrLit(span = p.linespan(1), str_value = p[1])

    def p_int_value(self, p):
        r"""
        value   : NUM_LIT
        """
        p[0] = NumLit(span = p.linespan(1), num_value = p[1])

    def p_var_value(self, p):
        r"""
        value   : VAR
        """
        p[0] = Var(span = p.linespan(1), name = p[1][1:])

    #def p_empty(self, p):
    #    r"empty :"
    #    pass

    #def p_error(self, p):
    #    print(t)

    def parse(self, **kwargs):
        return self.parser.parse(lexer=self.lexer.lexer, tracking=True, **kwargs)
