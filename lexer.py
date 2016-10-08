from collections import deque
import grammar
import inspect

# Returns a deque of tokens
def lex(inp):

    start = 0
    line = 0
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
        elif isinstance(token, Exception):
            raise token
        else:
            raise Exception("Invalid grammar")

    def append_token(token, s):
        nonlocal line
        cr = s.count("\n")
        tstream.append((token, s))

        if cr > 0:
            line += cr
            tstream.append(line)

    while start < len(inp):
        for r, token in tokens.items():
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
        else:
            # Found nothing, skip one character
            tstream.append(("T_UNKNOWN", inp[start]))
            start += 1

    return tstream