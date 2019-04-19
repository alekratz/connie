from connie.syn.ast import *


class Storage:
    def __init__(self):
        stack = []
        call_stack = []
        scope = {}

    def push(self, value: Value):
        self.stack.append(value)

    def pop(self) -> Value:
        return self.stack.pop()

    def lookup_name(self) -> Value:
        pass


class Run(Visitor):
    def __init__(self):
        self.storage = Storage()

    def run(self, body: Body):
        self.visit_body(body)

    def visit_body(self, body: Body):
        for ast in body:
            ast.visit(self)

    def visit_quote(self, quote: Quote):
        pass

    def visit_str_lit(self, str_lit: StrLit): pass
    def visit_num_lit(self, num_lit: NumLit): pass
    def visit_ident(self, ident: Ident): pass
    def visit_var(self, var: Var): pass
    def visit_assign(self, assign: Assign): pass
    def visit_sym(self, sym: Sym): pass
    def visit_list(self, ls: List): pass
