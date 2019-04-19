import abc
from dataclasses import dataclass
from typing import Sequence, Union
from connie.common import Span


@dataclass
class Ast(metaclass=abc.ABCMeta):
    span: Span

    @abc.abstractmethod
    def visit(self, visitor: 'Visitor'):
        """
        Implements the visitor pattern for this AST item.
        """


Body = Sequence[Ast]


@dataclass
class Literal(Ast):
    @property
    @abc.abstractmethod
    def value(self):
        """
        Gets the value of this AST item.
        """

    @property
    @abc.abstractmethod
    def value_kind(self):
        """
        Gets the AST runner's value kind.
        """


@dataclass
class Quote(Literal):
    body: Body

    @property
    def value(self):
        return self.body

    def visit(self, visitor: 'Visitor'):
        visitor.visit_quote(self)

    @property
    def value_kind(self):
        from connie.run.value import ValueKind
        return ValueKind.Quote


@dataclass
class StrLit(Literal):
    str_value: str

    @property
    def value(self):
        return self.str_value

    def visit(self, visitor: 'Visitor'):
        visitor.visit_str_lit(self)

    @property
    def value_kind(self):
        from connie.run.value import ValueKind
        return ValueKind.Str


@dataclass
class NumLit(Literal):
    num_value: int

    @property
    def value(self):
        return self.num_value

    def visit(self, visitor: 'Visitor'):
        visitor.visit_num_lit(self)

    @property
    def value_kind(self):
        from connie.run.value import ValueKind
        return ValueKind.Num


@dataclass
class Var(Literal):
    name: str

    @property
    def value(self):
        return self.name

    def visit(self, visitor: 'Visitor'):
        visitor.visit_var(self)

    @property
    def value_kind(self):
        from connie.run.value import ValueKind
        return ValueKind.Ref


@dataclass
class Assign(Ast):
    name: str

    def visit(self, visitor: 'Visitor'):
        visitor.visit_assign(self)


@dataclass
class Ident(Ast):
    name: str

    def visit(self, visitor: 'Visitor'):
        visitor.visit_ident(self)


@dataclass
class Sym(Ast):
    sym: str

    def visit(self, visitor: 'Visitor'):
        visitor.visit_sym(self)


@dataclass
class List(Literal):
    body: Body

    def visit(self, visitor: 'Visitor'):
        visitor.visit_list(self)

    @property
    def value(self):
        return self.body

    @property
    def value_kind(self):
        from connie.run.value import ValueKind
        return ValueKind.List


class Visitor:
    def visit_body(self, body: Body):
        for ast in body:
            ast.visit(self)

    def visit_quote(self, quote: Quote): pass
    def visit_str_lit(self, str_lit: StrLit): pass
    def visit_num_lit(self, num_lit: NumLit): pass
    def visit_ident(self, ident: Ident): pass
    def visit_var(self, var: Var): pass
    def visit_assign(self, assign: Assign): pass
    def visit_sym(self, sym: Sym): pass
    def visit_list(self, ls: List): pass
