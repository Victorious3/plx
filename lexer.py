from collections import deque
import grammar
import inspect

class Token:
    def __init__(self, token, content, line, char):
        self.token = token
        self.content = content
        self.line = line
        self.char = char

    def __str__(self):
        return "(" + str(self.line) + ", " + str(self.char) + " " + self.token + " : \"" + self.content + "\")"

# Returns a deque of tokens
def lex(inp):

    start = 0
    line = 0
    index = 0
    tstream = deque()
    tokens = grammar.tokens
    tstack = [tokens]

    grammar.init()

    def switch_token(token, s):
        nonlocal start, tokens
        if isinstance(token, str):
            append_token(token, s)
            start += len(s)
        elif isinstance(token, tuple):
            t = token[0]
            action = token[1]
            append_token(t, s)
            start += len(s)
            if action is None:
                tstack.pop()
                tokens = tstack[-1]
            elif isinstance(action, dict):
                tstack.append(action)
                tokens = action
        elif inspect.isgeneratorfunction(token):
            gen = token(inp[start:])
            for t, offset in gen:
                append_token(t, inp[start : start + offset])
                start += offset
        elif callable(token):
            t, offset = token(inp[start:])
            append_token(t, inp[start : start + offset])
            start += offset
        elif isinstance(token, BaseException):
            raise token
        else:
            raise Exception("Invalid grammar")

    def append_token(token, s):
        nonlocal line, index
        cr = s.count("\n")
        tstream.append(Token(token, s, line, index))

        if cr > 0:
            line += cr
        index += len(s)

    while start < len(inp):
        for r, token in tokens.items():
            try:
                if isinstance(r, str):
                    if len(r) > len(inp) - start: continue
                    if inp[start : start + len(r)] == r:
                        switch_token(token, r)
                        break
                else:
                    match = r.match(inp, start)
                    if match is not None:
                        m = match.group()
                        switch_token(token, m)
                        break
            except grammar.ParseException as e:
                print(str(line + 1) + ", " + str(start + 1) + ": " + str(e))
        else:
            # Found nothing, skip one character
            tstream.append(Token("T_UNKNOWN", inp[start], line, index))
            print(str(line + 1) + ", " + str(start + 1) + ": Unknown Symbol \"" + inp[start] + "\"")
            start += 1

    return tstream

def screen(tstream):
    return filter(lambda e: not e.token in ("T_WHITESPACE", "T_COMMENT", "T_MCOMMENT"), tstream)