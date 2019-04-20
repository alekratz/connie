import enum
from typing import Any


class ValueKind(enum.Enum):
    Str = enum.auto()
    Num = enum.auto()
    Bool = enum.auto()
    Quote = enum.auto()
    List = enum.auto()
    Ref = enum.auto()
    Builtin = enum.auto()


class Value:
    def __init__(self, kind: ValueKind, value: Any):
        self.kind = kind
        self.value = value

    @staticmethod
    def from_ast_value(value):
        return Value(value.value_kind, value.value)

    def __str__(self) -> str:
        if self.kind in (ValueKind.Str, ValueKind.Num, ValueKind.Bool):
            return str(self.value)
        elif self.kind == ValueKind.Ref:
            return '<named reference "{}">'.format(self.value)
        elif self.kind == ValueKind.List:
            return "[" + ", ".join(map(str, self.value)) + "]"
        elif self.kind == ValueKind.Builtin:
            return '<builtin function "{}">'.format(self.value.__name__)
        elif self.kind == ValueKind.Quote:
            return "<quoted value>"


def check_types(expected, got):
    """
    Checks a list of expected types against another list of gathered types.

    :param expected: the expected types. This should be a tuple of N types or typesets (a tuple of
                     allowed types).
    :param got: the list of types that are being checked.

    The implementation is dense (sorry).
    """
    assert len(got) == len(expected)
    bindings = {}
    for g, e in zip(got, expected):
        if isinstance(e, str):
            if e in bindings:
                ty = bindings[e]
                if isinstance(ty, tuple):
                    if g not in ty:
                        return False
                elif g != ty:
                    return False
            else:
                bindings[e] = g
        elif isinstance(e, tuple):
            if g not in e:
                return False
        else:
            assert isinstance(e, ValueKind)
            if g != e:
                return False
    return True
