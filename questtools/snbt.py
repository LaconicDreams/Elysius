"""SNBT reader/writer matching the format FTB Quests 2001.x writes.

Values keep their NBT type so files round-trip exactly:
  Byte(1) -> 1b, Short(1) -> 1s, Long(3) -> 3L, Float(1.0) -> 1.0f, Double(0.0) -> 0.0d,
  plain int -> 3, bool -> true/false, str -> "text", dict -> compound, list -> list.
"""

import re


class Byte(int):
    suffix = "b"


class Short(int):
    suffix = "s"


class Long(int):
    suffix = "L"


class Float(float):
    suffix = "f"


class Double(float):
    suffix = "d"


class TypedArray(list):
    """[I; 1, 2, 3] style arrays. kind is 'B', 'I' or 'L'."""

    def __init__(self, kind, items=()):
        super().__init__(items)
        self.kind = kind


class SNBTError(Exception):
    def __init__(self, msg, line, col):
        super().__init__(f"line {line}, col {col}: {msg}")
        self.msg, self.line, self.col = msg, line, col


_NUM_RE = re.compile(r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?([bBsSlLfFdD]?)$")
_BARE_RE = re.compile(r"[A-Za-z0-9_\-.+]+")


class _Parser:
    def __init__(self, text):
        self.s = text.lstrip("\ufeff")
        self.i = 0
        self.n = len(self.s)

    def pos(self, i=None):
        i = self.i if i is None else i
        line = self.s.count("\n", 0, i) + 1
        col = i - (self.s.rfind("\n", 0, i) + 1) + 1
        return line, col

    def err(self, msg, i=None):
        raise SNBTError(msg, *self.pos(i))

    def skip(self):
        s, n = self.s, self.n
        while self.i < n:
            c = s[self.i]
            if c in " \t\r\n,":
                self.i += 1
            elif c == "#" or s.startswith("//", self.i):  # tolerate comments
                j = s.find("\n", self.i)
                self.i = n if j < 0 else j + 1
            else:
                break

    def parse(self):
        self.skip()
        v = self.value()
        self.skip()
        if self.i < self.n:
            self.err(f"unexpected '{self.s[self.i]}' after the end of the top-level value")
        return v

    def value(self):
        self.skip()
        if self.i >= self.n:
            self.err("unexpected end of file")
        c = self.s[self.i]
        if c == "{":
            return self.compound()
        if c == "[":
            return self.list_()
        if c in "\"'":
            return self.string()
        if c in "}]":
            self.err(f"unexpected '{c}' (no matching opening bracket?)")
        return self.bare()

    def compound(self):
        start = self.i
        self.i += 1
        out = {}
        while True:
            self.skip()
            if self.i >= self.n:
                self.err("'{' is never closed", start)
            c = self.s[self.i]
            if c == "}":
                self.i += 1
                return out
            if c == "]":
                self.err("found ']' but expected '}' to close the '{' opened at line %d" % self.pos(start)[0])
            key_at = self.i
            key = self.string() if c in "\"'" else self.bare_word()
            self.skip_ws()
            if self.i >= self.n or self.s[self.i] != ":":
                self.err(f"expected ':' after key '{key}'")
            self.i += 1
            if key in out:
                self.err(f"duplicate key '{key}' in the same compound", key_at)
            out[key] = self.value()

    def list_(self):
        start = self.i
        self.i += 1
        m = re.match(r"\s*([BIL])\s*;", self.s[self.i:self.i + 8])
        out = TypedArray(m.group(1)) if m else []
        if m:
            self.i += m.end()
        while True:
            self.skip()
            if self.i >= self.n:
                self.err("'[' is never closed", start)
            c = self.s[self.i]
            if c == "]":
                self.i += 1
                return out
            if c == "}":
                self.err("found '}' but expected ']' to close the '[' opened at line %d" % self.pos(start)[0])
            v = self.value()
            out.append(int(v) if isinstance(out, TypedArray) else v)
            self.skip_ws()
            if self.i < self.n and self.s[self.i] == ":":
                self.err("missing ']' to close the '[' opened at line %d (found a 'key:' inside the list)"
                         % self.pos(start)[0])

    def skip_ws(self):
        while self.i < self.n and self.s[self.i] in " \t":
            self.i += 1

    def string(self):
        q = self.s[self.i]
        start = self.i
        self.i += 1
        buf = []
        s = self.s
        while True:
            if self.i >= self.n:
                self.err("string is never closed", start)
            c = s[self.i]
            if c == "\\":
                nxt = s[self.i + 1:self.i + 2]
                buf.append({"n": "\n", "t": "\t", "r": "\r"}.get(nxt, nxt))
                self.i += 2
            elif c == q:
                self.i += 1
                return "".join(buf)
            elif c == "\n":
                self.err("line break inside a string (missing closing quote?)", start)
            else:
                buf.append(c)
                self.i += 1

    def bare_word(self):
        m = _BARE_RE.match(self.s, self.i)
        if not m:
            self.err(f"unexpected character '{self.s[self.i]}'")
        self.i = m.end()
        return m.group(0)

    def bare(self):
        start = self.i
        word = self.bare_word()
        if word == "true":
            return True
        if word == "false":
            return False
        m = _NUM_RE.match(word)
        if m:
            suf = m.group(1)
            body = word[:-1] if suf else word
            try:
                if suf in "bB" and suf:
                    return Byte(int(body))
                if suf in "sS" and suf:
                    return Short(int(body))
                if suf in "lL" and suf:
                    return Long(int(body))
                if suf in "fF" and suf:
                    return Float(float(body))
                if suf in "dD" and suf:
                    return Double(float(body))
                if re.fullmatch(r"[-+]?\d+", body):
                    return int(body)
                return Double(float(body))
            except ValueError:
                self.err(f"bad number '{word}'", start)
        return word  # unquoted string


def loads(text):
    return _Parser(text).parse()


def load(path):
    with open(path, encoding="utf-8") as f:
        return loads(f.read())


# ---------------------------------------------------------------- writer

def _fmt_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def _fmt_scalar(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (Byte, Short, Long)):
        return f"{int(v)}{v.suffix}"
    if isinstance(v, (Float, Double)):
        return f"{float(v)!r}{v.suffix}"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return f"{v!r}d"
    if isinstance(v, str):
        return _fmt_str(v)
    raise TypeError(f"can't write {type(v).__name__} to SNBT")


def _write(v, ind, out):
    t = "\t"
    if isinstance(v, dict):
        if not v:
            out.append("{ }")
            return
        out.append("{\n")
        for k in sorted(v):
            key = k if _BARE_RE.fullmatch(k) else _fmt_str(k)
            out.append(t * (ind + 1) + key + ": ")
            _write(v[k], ind + 1, out)
            out.append("\n")
        out.append(t * ind + "}")
    elif isinstance(v, TypedArray):
        out.append(f"[{v.kind}; " + ", ".join(str(x) for x in v) + "]")
    elif isinstance(v, list):
        if not v:
            out.append("[ ]")
        elif len(v) == 1 and not isinstance(v[0], list):
            out.append("[")
            if isinstance(v[0], dict):
                sub = []
                _write(v[0], ind, sub)
                out.append("".join(sub))
            else:
                out.append(_fmt_scalar(v[0]))
            out.append("]")
        else:
            out.append("[\n")
            for x in v:
                out.append(t * (ind + 1))
                _write(x, ind + 1, out)
                out.append("\n")
            out.append(t * ind + "]")
    else:
        out.append(_fmt_scalar(v))


def dumps(v):
    out = []
    _write(v, 0, out)
    return "".join(out) + "\n"


def dump(v, path):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(dumps(v))
