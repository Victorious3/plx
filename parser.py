class TokenStream:
    def __init__(self, tlist):
        self.tlist = tlist
        self.index = 0

    def peek(self, offset = 1):
        return self.tlist[self.index + offset]

    def pop(self, offset = 1):
        oi = self.index
        self.index += offset
        return self.tlist[oi]

def line_break_or_eof(tstream):
    if tstream.index + 1 == len(tstream.tlist):
        return True
    line = tstream.peek(0).line
    return line > tstream.peek().line

def parse(tlist):
    tstream = TokenStream(tlist)
    tree = ("root")
    while True:
        try:
            nxt = tstream.pop()
            if nxt.token == "T_KEY_CLASS":
                tree += parse_class(tstream)
            else:
                tree += parse_expression(tstream)

            if not line_break_or_eof(tstream):
                error()
        except IndexError:
            break
    return tree

def parse_ident(tstream):
    pass

def parse_fcall(tstream):
    pass

def parse_expression(tstream):
    if tstream.peek().token == "T_KEY_IF":
        return parse_if(tstream)
    else: return parse_or(tstream)

def parse_or(tstream):
    a = parse_and(tstream)
    while tstream.peek().token == "T_KEY_OR":
        tstream.pop()
        b = parse_and(tstream)
        a = ("or", a, b)
    return a

def parse_and(tstream):
    a = parse_eq(tstream)
    while tstream.peek().token == "T_KEY_AND":
        tstream.pop()
        b = parse_eq(tstream)
        a = ("and", a, b)
    return a

def parse_eq(tstream):
    a = parse_cmp(tstream)
    while tstream.peek().token in ("T_KEY_IS", "T_EQ", "T_NOT_EQ"):
        op = tstream.pop()
        if tstream.peek().token == "T_KEY_NOT":
            tstream.pop()
            b = parse_cmp(tstream)
            a = ("n_is", a, b)
        else:
            b = parse_cmp(tstream)
            a = ("is" if op == "T_KEY_IS" else ("eq" if op == "T_EQ" else "n_eq"), a, b)
    return a

def parse_cmp(tstream):
    a = parse_bor_bxor(tstream)
    while tstream.peek().token in ("T_LT", "T_LT_EQ", "T_HT", "T_HT_EQ"):
        op = tstream.pop()
        b = parse_bor_bxor(tstream)
        a = ("lt" if op == "T_LT" else ("lt_eq" if op == "T_LT_EQ" else ("ht" if op == "T_HT" else "ht_eq")), a, b)
    return a

def parse_bor_bxor(tstream):
    a = parse_band(tstream)
    while tstream.peek().token in ("T_CARET", "T_PIPE"):
        op = tstream.pop()
        b = parse_band(tstream)
        a = ("b_xor" if op == "T_CARET" else "b_or", a, b)
    return a

def parse_band(tstream):
    a = parse_bshift(tstream)
    while tstream.peek().token == "T_AMPERSAND":
        tstream.pop()
        b = parse_bshift(tstream)
        a = ("b_and", a, b)
    return a

def parse_bshift(tstream):
    pass

def parse_class(tstream):
    pass

def parse_trait(tstream):
    pass

def parse_struct(tstream):
    pass

def parse_if(tstream):
    pass

def parse_for(tstream):
    pass

