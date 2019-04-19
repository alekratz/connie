from typing import Optional


def unescape(s: str) -> str:
    """
    Resolves all escape sequences for the given string.
    """
    mapping = {
        'n': '\n',
        'r': '\r',
        't': '\t',
        '\\': '\\',
        '"': '"',
        "'": "'",
    }
    parts = s.split('\\')
    new = parts[0]
    for p in parts[1:]:
        new += mapping[p[0]] + p[1:]
    return new


class Lex:
    tokens = (
        'STR_LIT',
        'NUM_LIT',
        'IDENT',
        'SET',
        'VAR',
        #'LPAREN',
        #'RPAREN',
        'LBRACE',
        'RBRACE',
        'LBRACKET',
        'RBRACKET',
        'SYM',
    )

    def __init__(self, source: str, source_name: Optional[str]=None) -> None:
        import ply.lex as lex
        self.lexer = lex.lex(module=self)
        self.lexer.input(source)
        self.source = source
        self.source_name = source_name
        self.code_layers = 0

    def t_STR_LIT(self, t):
        r"""
            " ( [^"\\] | \\[rnt\\"'] )* "   # Double-quoted strings
        |   ' ( [^'\\] | \\[rnt\\"'] )* '   # Single-quoted strings
        """
        t.value = unescape(t.value[1:-1])
        return t

    def t_NUM_LIT(self, t):
        r"""
            (0x[a-f0-9]+)
        |   (0b[01]+)
        |   (0o[0-7]+)
        |   [0-9]+
        """
        val = t.value.lower()
        if val.startswith('0x'):
            t.value = int(val[2:], 16)
        elif val.startswith('0o'):
            t.value = int(val[2:], 8)
        elif val.startswith('0b'):
            t.value = int(val[2:], 2)
        else:
            t.value = int(val)
        return t

    t_IDENT = r"[a-zA-Z_][a-zA-Z-_0-9]*"
    t_SET = r"=" + t_IDENT
    t_VAR = r"\$[a-zA-Z-_0-9]+"
    t_SYM = r'[!%&*+-./:<=>?@\\^`|~,]+'
    #t_LPAREN = r'\('
    #t_RPAREN = r'\('
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'

    def t_COMMENT(self, t):
        r'\#[^\n]*'
        t.lexer.lineno += 1
        return None

    t_ignore = "\t "

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count('\n')

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        raise SyntaxError()

    def __iter__(self):
        while True:
            tok = self.lexer.token()
            if tok:
                yield tok
            else:
                break
