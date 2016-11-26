from re import compile as regex
from collections import OrderedDict

class ParseException(Exception):
    pass

indent = [0]

def init():
    global indent
    indent = [0]

def back(s):
    return s, None

def kw(keyword):
    return regex("(" + keyword + ")(?=$|\s)")

def parse_comment(inp):
    stack = 0
    offset = 0
    pattern = regex(r'(\/\*)|(\*\/)')
    while True:
        match = pattern.search(inp, offset)
        if match is None:
            raise ParseException("Hit end of file while parsing comment")
        if match.group(1):
            stack += 1
        else:
            stack -= 1
        offset += match.start() + 2
        if stack == 0: break
    return "T_MCOMMENT", offset

# TODO Doc comment?

def parse_indent(inp):
    global indent
    i = indent[-1]
    pattern = regex(r'\s*')
    match = pattern.match(inp)
    curr = len(match.group().replace("\t", "    ").replace("\n", ""))
    l = curr + 1

    if curr > i:
        indent.append(curr)
        yield "T_INDENT", l
    elif curr < i:
        indent.pop()
        while True:
            i = indent[-1]
            if curr < i:
                indent.pop()
                yield "T_DEDENT", l
            else:
                yield "T_DEDENT", l
                break
            l = 0
    else:
        yield "T_WHITESPACE", l

tokens = OrderedDict([
    # T_INDENT
    # T_DEDENT

    # T_ISTRING_CONTINUE
    # T_ISTRING_END

    (regex(r'\s+(?=\n)'), "T_WHITESPACE"),
    (regex(r'(\n\s*)|(^\s+)'), parse_indent),
    (regex(r'\s+'), "T_WHITESPACE"),
    (regex(r'\/\/.*(?=\n|$)'), "T_COMMENT"),

    ("/*", parse_comment),
    ("*/", ParseException("Unexpected symbol")),

    ("{", "T_OPEN_BRACKETS"),
    ("}", "T_CLOSE_BRACKETS"),
    ("(", "T_OPEN_PAREN"),
    (")", "T_CLOSE_PAREN"),
    ("[", "T_OPEN_SQUARE"),
    ("]", "T_CLOSE_SQUARE"),
    (",", "T_COMMA"),
    ("...", "T_ELLIPSE"),
    ("..", "T_RANGE"),
    (".", "T_DOT"),
    (",", "T_COLON"),
    (";", "T_SEMICOLON"),
    ("\\", "T_BACK"),
    ("->", "T_ARROW"),

    (kw("if"), "T_KEY_IF"),
    (kw("else"), "T_KEY_ELSE"),
    (kw("do"), "T_KEY_DO"),
    (kw("break"), "T_KEY_BREAK"),
    (kw("continue"), "T_KEY_CONTINUE"),
    (kw("import"), "T_KEY_IMPORT"),
    (kw("from"), "T_KEY_FROM"),
    (kw("as"), "T_KEY_AS"),
    (kw("while"), "T_KEY_WHILE"),
    (kw("for"), "T_KEY_FOR"),
    (kw("in"), "T_KEY_IN"),
    (kw("extends"), "T_KEY_EXTENDS"),
    (kw("with"), "T_KEY_WITH"),
    (kw("var"), "T_KEY_VAR"),
    (kw("const"), "T_KEY_CONST"),
    (kw("return"), "T_KEY_RETURN"),
    (kw("def"), "T_KEY_DEF"),
    (kw("struct"), "T_KEY_STRUCT"),
    (kw("trait"), "T_KEY_TRAIT"),
    (kw("class"), "T_KEY_CLASS"),
    (kw("implement"), "T_KEY_IMPLEMENT"),
    (kw("module"), "T_KEY_MODULE"),
    (kw("match"), "T_KEY_MATCH"),
    (kw("case"), "T_KEY_CASE"),
    (kw("type"), "T_KEY_TYPE"),
    (kw("true"), "T_TRUE"),
    (kw("delete"), "T_DELETE"),
    (kw("new"), "T_NEW"),

    (kw("false"), "T_FALSE"),
    (kw("null"), "T_NULL"),

    (kw("is"), "T_IS"),
    (kw("and"), "T_AND"),
    (kw("or"), "T_OR"),
    (kw("not"), "T_NOT"),

    ("==", "T_EQ"),
    ("!=", "T_NOT_EQ"),
    ("<=", "T_LT_EQ"),
    ("<<", "T_LSHFT"),
    ("<", "T_LT"),
    (">=", "T_HT_EQ"),
    (">>>", "T_URSHFT"),
    (">>", "T_RSHFT"),
    (">", "T_HT"),
    ("++", "T_INCR"),
    ("+=", "T_PLUS_EQ"),
    ("+", "T_PLUS"),
    ("--", "T_DECR"),
    ("-=", "T_MINUS_EQ"),
    ("-", "T_MINUS"),
    ("**=", "T_POW_EQ"),
    ("**", "T_POW"),
    ("*=", "T_MUL_EQ"),
    ("*", "T_MUL"),
    ("/=", "T_DIV_EQ"),
    ("/", "T_DIV"),
    ("~=", "T_TILDE_EQ"),
    ("~", "T_TILDE"),
    ("&=", "T_AMPERSAND_EQ"),
    ("&", "T_AMPERSAND"),
    ("|=", "T_PIPE_EQ"),
    ("|", "T_PIPE"),
    ("@", "T_AT"),
    ("^=", "T_CARET_EQ"),
    ("^", "T_CARET"),
    ("=", "T_ASSIGN"),

    ("!!", "T_AUTOCAST"),
    ("!", "T_CAST"),
    ("?", "T_QMARK"),

    (regex(r'(0[xbo][0-9A-F]+)|(([0-9]+\.[0-9]+)([Ee][0-9]+)?|([0-9]+)([Ee][0-9]+)?)'), "T_NUMBER"),
    (regex(r'[_a-zA-Z][_a-zA-Z0-9]*'), "T_ID"),

    # Interpolated string without any interpolation used
    (regex(r'\$"(\\.|[^"$])*"'), "T_ISTRING"),

    (regex(r'\$"(\\.|[^"$])*\$'), ("T_ISTRING_START", OrderedDict([
        (regex(r'[_a-zA-Z][_a-zA-Z0-9]*'), "T_ID"),
        (".", "T_DOT"),
        (regex(r'(\\.|[^"$])*\$'), "T_ISTRING_CONTINUE"),
        (regex(r'(\\.|[^"$])*"'), back("T_ISTRING_END"))
    ]))),

    (regex(r'"(\\.|[^"])*"'), "T_STRING")
])
