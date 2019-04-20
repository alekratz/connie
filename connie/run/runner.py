from pathlib import Path
import random
import math
import os
from connie.run import util
from connie.run.value import *
from connie.syn.ast import *
from connie.syn.parse import Parse


IO_BUF_SIZE = 4096


class Storage:
    def __init__(self):
        self.stack = [[]]
        self.call_stack = []
        self.scope = [
            {
                name: Value(ValueKind.Builtin, builtin)
                for name, builtin in BUILTINS.items()
            }
        ]

    def peek(self) -> Value:
        return self.stack[-1][-1]

    def push(self, value: Value):
        assert isinstance(value, Value), "attempted to push non-Value type (%s): %s" % (
            type(value),
            value,
        )
        self.stack[-1].append(value)

    def pop(self) -> Value:
        value = self.stack[-1].pop()
        if value.kind == ValueKind.Ref:
            return self.get_name(value.value)
        else:
            return value

    def push_stack_layer(self):
        self.stack.append([])

    def pop_stack_layer(self):
        return self.stack.pop()

    def push_scope(self):
        self.scope.append({})

    def pop_scope(self):
        return self.scope.pop()

    def get_name(self, name: str) -> Value:
        for scope in reversed(self.scope):
            if name in scope:
                return scope[name]
        raise Exception("unknown name `{}`".format(name))

    def set_name(self, name: str, value: Value):
        assert isinstance(
            value, Value
        ), "attempted to assign non-Value type (%s): %s" % (type(value), value)
        self.scope[-1][name] = value


class Run(Visitor):
    def __init__(self, search_paths=None):
        self.storage = Storage()
        self.search_paths = (search_paths or []) + [Path.cwd()]

    def run_path(self, path: Path):
        found = util.search_path(path, self.search_paths)
        if found is None:
            raise Exception('could not find import path "{}"'.format(path))
        path = found
        try:
            with open(path) as fp:
                contents = fp.read()
        except Exception as ex:
            raise Exception('could not import "{}": {}'.format(path, ex))
        self.search_paths = [path.parent] + self.search_paths
        self.run_str(contents, path)
        self.search_paths = self.search_paths[1:]

    def run_str(self, source: str, source_name: str):
        body = Parse(source, source_name).parse()
        self.run(body)

    def run(self, body: Body):
        for ast in body:
            ast.visit(self)

    def call(self, value: Value):
        if value.kind == ValueKind.Quote:
            self.visit_body(value.value)
        elif value.kind == ValueKind.Builtin:
            value.value(self)
        else:
            self.storage.push(value)

    def visit_body(self, body: Body):
        self.storage.push_scope()
        for ast in body:
            ast.visit(self)
        self.storage.pop_scope()

    def visit_quote(self, quote: Quote):
        self.storage.push(Value.from_ast_value(quote))

    def visit_str_lit(self, str_lit: StrLit):
        self.storage.push(Value.from_ast_value(str_lit))

    def visit_num_lit(self, num_lit: NumLit):
        self.storage.push(Value.from_ast_value(num_lit))

    def visit_ident(self, ident: Ident):
        value = self.storage.get_name(ident.name)
        self.call(value)

    def visit_var(self, var: Var):
        self.storage.push(Value.from_ast_value(var))

    def visit_assign(self, assign: Assign):
        value = self.storage.pop()
        self.storage.set_name(assign.name, value)

    def visit_sym(self, sym: Sym):
        value = self.storage.get_name(sym.sym)
        self.call(value)

    def visit_list(self, ls: List):
        self.storage.push_stack_layer()
        self.visit_body(ls.value)
        layer = self.storage.pop_stack_layer()
        self.storage.push(Value(ValueKind.List, layer))

    def builtin_input(self):
        value = input()
        self.storage.push(Value(ValueKind.Str, value))

    def builtin_random(self):
        value = Value(ValueKind.Num, random.random())
        self.storage.push(value)

    def builtin_ceil(self):
        value = self.storage.pop()
        if value.kind != ValueKind.Num:
            raise Exception(
                "invalid `ceil` call on non-numeric value `{}`".format(value.kind)
            )
        value.value = math.ceil(value.value)
        self.storage.push(value)

    def builtin_floor(self):
        value = self.storage.pop()
        if value.kind != ValueKind.Num:
            raise Exception(
                "invalid `floor` call on non-numeric value `{}`".format(value.kind)
            )
        value.value = math.floor(value.value)
        self.storage.push(value)

    def builtin_index(self):
        index = self.storage.pop()
        if index.kind != ValueKind.Num:
            raise Exception(
                "invalid `index` call on index kind `{}`".format(index.kind)
            )
        value = self.storage.pop()
        if value.kind not in (ValueKind.Quote, ValueKind.Str, ValueKind.List):
            raise Exception(
                "invalid `index` call on non-indexable value kind `{}`".format(
                    value.kind
                )
            )
        if value.kind == ValueKind.Quote:
            single = value.value[index.value]
            result = Value(ValueKind.Quote, [single])
        elif value.kind == ValueKind.Str:
            single = value.value[index.value]
            result = Value(ValueKind.Str, single)
        elif value.kind == ValueKind.List:
            result = value.value[index.value]
        else:
            assert False, "Invalid indexed value kind %s" % value.kind
        self.storage.push(result)

    def builtin_len(self):
        value = self.storage.pop()
        if value.kind not in (ValueKind.Quote, ValueKind.Str, ValueKind.List):
            raise Exception(
                "invalid `len` call on lengthless value kind `{}`".format(value.kind)
            )
        self.storage.push(Value(ValueKind.Num, len(value.value)))

    def builtin_int(self):
        value = self.storage.pop()
        if value.kind not in (ValueKind.Num, ValueKind.Str):
            raise Exception("invalid `int` call on value kind `{}`".format(value.kind))
        self.storage.push(Value(ValueKind.Num, int(value.value)))

    def builtin_str(self):
        value = self.storage.pop()
        self.storage.push(Value(ValueKind.Str, str(value)))

    def builtin_dupe(self):
        # (T) -> T T
        value = self.storage.peek()
        self.storage.push(value)

    def builtin_mult(self):
        # (int, int) -> int
        # (int, T) -> T
        # (T, int) -> T
        lhs = self.storage.pop()
        rhs = self.storage.pop()

        ints = check_types((ValueKind.Num, ValueKind.Num), (lhs.kind, rhs.kind))
        int_t = check_types((ValueKind.Num, "T"), (lhs.kind, rhs.kind))
        t_int = check_types(("T", ValueKind.Num), (lhs.kind, rhs.kind))

        any_type = ints or int_t or t_int
        if not any_type:
            raise Exception(
                "invalid multiplication on value kinds `{}` and `{}` - at least one "
                "value kind must be numeric".format(lhs.kind, rhs.kind)
            )
        result = lhs.value * rhs.value
        if ints:
            out_type = ValueKind.Num
        elif int_t:
            out_type = rhs.kind
        else:
            out_type = rhs.kind
        self.storage.push(Value(out_type, result))

    def builtin_plus(self):
        # (T, T) -> T
        lhs = self.storage.pop()
        rhs = self.storage.pop()
        valid_types = check_types(("T", "T"), (lhs.kind, rhs.kind))
        if not valid_types:
            raise Exception(
                "invalid addition on value kinds `{}` and `{}` - both values must "
                "be of the same type".format(lhs.kind, rhs.kind)
            )
        if lhs.kind == ValueKind.Bool:
            result = lhs.value and rhs.value
        else:
            result = lhs.value + rhs.value
        self.storage.push(Value(lhs.kind, result))

    def builtin_equals(self):
        # (T, U) -> int
        lhs = self.storage.pop()
        rhs = self.storage.pop()
        self.storage.push(Value(ValueKind.Bool, lhs.value == rhs.value))

    def builtin_not_equals(self):
        # (T, U) -> int
        lhs = self.storage.pop()
        rhs = self.storage.pop()
        self.storage.push(Value(ValueKind.Bool, lhs.value != rhs.value))

    def builtin_bang(self):
        # (T) -> int
        value = self.storage.pop()
        self.storage.push(Value(ValueKind.Bool, not bool(value.value)))

    def builtin_select(self):
        # (List) -> ?
        value = self.storage.pop()
        if value.kind != ValueKind.List:
            raise Exception(
                "invalid `select` call on value kind `{}`: "
                "must be a list".format(value.kind)
            )
        default = None
        if len(value.value) % 2 == 1:
            default = value.value.pop()
        selected = default
        for i in range(0, len(value.value), 2):
            cond = value.value[i + 1]
            self.call(cond)
            result = self.storage.pop()
            if bool(result.value):
                selected = value.value[i]
                break

        if selected is not None:
            self.call(selected)

    def builtin_import(self):
        value = self.storage.pop()
        if value.kind != ValueKind.Str:
            raise Exception(
                "invalid `import` call on value kind `{}`: "
                "must be a string".format(value.kind)
            )
        path = Path(value.value)
        self.run_path(path)

    def builtin_read(self):
        handle = self.storage.pop()
        if handle.kind == ValueKind.Num:
            # TODO sink/source impl?
            content = bytes()
            hdl = handle.value
            while True:
                got = os.read(hdl, IO_BUF_SIZE)
                if not got:
                    break
                content += got
            content = content.decode()
        elif handle.kind == ValueKind.Str:
            # open r vs. rb?
            # encoding?
            with open(handle.value) as fp:
                content = fp.read()
        self.storage.push(Value(ValueKind.Str, content))

    def builtin_write(self):
        handle = self.storage.pop()
        buf = self.storage.pop()
        if buf.kind != ValueKind.Str:
            raise Exception(
                "invalid `write` call on value kind `{}`: "
                "must be a string".format(buf.kind)
            )
        if handle.kind == ValueKind.Num:
            content = buf.value.encode()
            hdl = handle.value
            while content:
                wrote = os.write(hdl, content)
                content = content[wrote:]
        elif handle.kind == ValueKind.Str:
            with open(handle.value) as fp:
                fp.write(buf)


BUILTINS = {
    # to remove
    "input": Run.builtin_input,

    "random": Run.builtin_random,
    "ceil": Run.builtin_ceil,
    "floor": Run.builtin_floor,
    "index": Run.builtin_index,
    "len": Run.builtin_len,
    "int": Run.builtin_int,
    "str": Run.builtin_str,
    "select": Run.builtin_select,
    "import": Run.builtin_import,

    # TODO readb, writeb
    "read": Run.builtin_read,
    "write": Run.builtin_write,
    #"eval": Run.builtin_eval,

    "^": Run.builtin_dupe,
    "*": Run.builtin_mult,
    "+": Run.builtin_plus,
    "==": Run.builtin_equals,
    "!=": Run.builtin_not_equals,
    "!": Run.builtin_bang,
}
