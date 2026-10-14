"""Binary NBT (gzip) reader/writer for structure files. Uses the typed values from snbt.py:
Byte, Short, int (Int), Long, Float, Double, str, list, dict, TypedArray('B'|'I'|'L')."""

import gzip
import io
import struct

from snbt import Byte, Double, Float, Long, Short, TypedArray

END, BYTE, SHORT, INT, LONG, FLOAT, DOUBLE, BYTE_ARRAY, STRING, LIST, COMPOUND, INT_ARRAY, LONG_ARRAY = range(13)


class NBTList(list):
    """A list that remembers its element tag type (needed for empty lists)."""

    def __init__(self, items=(), tag=None):
        super().__init__(items)
        self.tag = tag


def _tag_of(v):
    if isinstance(v, bool):
        return BYTE
    if isinstance(v, Byte):
        return BYTE
    if isinstance(v, Short):
        return SHORT
    if isinstance(v, Long):
        return LONG
    if isinstance(v, Float):
        return FLOAT
    if isinstance(v, (Double, float)):
        return DOUBLE
    if isinstance(v, int):
        return INT
    if isinstance(v, str):
        return STRING
    if isinstance(v, TypedArray):
        return {"B": BYTE_ARRAY, "I": INT_ARRAY, "L": LONG_ARRAY}[v.kind]
    if isinstance(v, list):
        return LIST
    if isinstance(v, dict):
        return COMPOUND
    raise TypeError(f"can't write {type(v).__name__} as NBT")


def _w(out, tag, v):
    if tag == BYTE:
        out.write(struct.pack(">b", int(v)))
    elif tag == SHORT:
        out.write(struct.pack(">h", v))
    elif tag == INT:
        out.write(struct.pack(">i", v))
    elif tag == LONG:
        out.write(struct.pack(">q", v))
    elif tag == FLOAT:
        out.write(struct.pack(">f", v))
    elif tag == DOUBLE:
        out.write(struct.pack(">d", v))
    elif tag == STRING:
        b = v.encode("utf-8")
        out.write(struct.pack(">H", len(b)) + b)
    elif tag in (BYTE_ARRAY, INT_ARRAY, LONG_ARRAY):
        fmt = {BYTE_ARRAY: "b", INT_ARRAY: "i", LONG_ARRAY: "q"}[tag]
        out.write(struct.pack(">i", len(v)) + struct.pack(">" + fmt * len(v), *v))
    elif tag == LIST:
        et = getattr(v, "tag", None) or (_tag_of(v[0]) if v else END)
        out.write(struct.pack(">bi", et, len(v)))
        for x in v:
            _w(out, et, x)
    elif tag == COMPOUND:
        for k, x in v.items():
            t = _tag_of(x)
            out.write(struct.pack(">b", t))
            _w(out, STRING, k)
            _w(out, t, x)
        out.write(b"\x00")


def _r(f, tag):
    if tag == BYTE:
        return Byte(struct.unpack(">b", f.read(1))[0])
    if tag == SHORT:
        return Short(struct.unpack(">h", f.read(2))[0])
    if tag == INT:
        return struct.unpack(">i", f.read(4))[0]
    if tag == LONG:
        return Long(struct.unpack(">q", f.read(8))[0])
    if tag == FLOAT:
        return Float(struct.unpack(">f", f.read(4))[0])
    if tag == DOUBLE:
        return Double(struct.unpack(">d", f.read(8))[0])
    if tag == STRING:
        n = struct.unpack(">H", f.read(2))[0]
        return f.read(n).decode("utf-8", "replace")
    if tag in (BYTE_ARRAY, INT_ARRAY, LONG_ARRAY):
        n = struct.unpack(">i", f.read(4))[0]
        fmt, size, kind = {BYTE_ARRAY: ("b", 1, "B"), INT_ARRAY: ("i", 4, "I"), LONG_ARRAY: ("q", 8, "L")}[tag]
        return TypedArray(kind, struct.unpack(">" + fmt * n, f.read(size * n)))
    if tag == LIST:
        et, n = struct.unpack(">bi", f.read(5))
        return NBTList([_r(f, et) for _ in range(n)], et)
    if tag == COMPOUND:
        out = {}
        while True:
            t = struct.unpack(">b", f.read(1))[0]
            if t == END:
                return out
            k = _r(f, STRING)
            out[k] = _r(f, t)
    raise ValueError(f"bad NBT tag {tag}")


def loads(data):
    if data[:2] == b"\x1f\x8b":
        data = gzip.decompress(data)
    f = io.BytesIO(data)
    t = struct.unpack(">b", f.read(1))[0]
    if t != COMPOUND:
        raise ValueError("root tag is not a compound")
    _r(f, STRING)
    return _r(f, COMPOUND)


def load(path):
    with open(path, "rb") as fh:
        return loads(fh.read())


def dumps(root):
    out = io.BytesIO()
    out.write(struct.pack(">b", COMPOUND))
    _w(out, STRING, "")
    _w(out, COMPOUND, root)
    return gzip.compress(out.getvalue(), mtime=0)


def dump(root, path):
    with open(path, "wb") as fh:
        fh.write(dumps(root))
