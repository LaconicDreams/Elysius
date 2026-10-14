"""Minimal PNG read/write (8-bit RGB/RGBA, non-interlaced), enough to recolor Minecraft textures
without installing an image library."""

import colorsys
import struct
import zlib


def read(data):
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    pos, idat, w = 8, b"", None
    while pos < len(data):
        ln, typ = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + ln]
        pos += 12 + ln
        if typ == b"IHDR":
            w, h, depth, ctype, _, _, inter = struct.unpack(">IIBBBBB", body)
            if depth != 8 or ctype not in (2, 6) or inter:
                raise ValueError(f"unsupported PNG (depth {depth}, color type {ctype}, interlace {inter})")
            bpp = 4 if ctype == 6 else 3
        elif typ == b"IDAT":
            idat += body
        elif typ == b"IEND":
            break
    raw = zlib.decompress(idat)
    stride = w * bpp
    rows, prev, i = [], bytearray(stride), 0
    for _ in range(h):
        f = raw[i]
        line = bytearray(raw[i + 1:i + 1 + stride])
        i += 1 + stride
        for x in range(stride):
            a = line[x - bpp] if x >= bpp else 0
            b = prev[x]
            c = prev[x - bpp] if x >= bpp else 0
            if f == 1:
                line[x] = (line[x] + a) & 255
            elif f == 2:
                line[x] = (line[x] + b) & 255
            elif f == 3:
                line[x] = (line[x] + (a + b) // 2) & 255
            elif f == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        rows.append(line)
        prev = line
    px = []
    for line in rows:
        for x in range(w):
            p = line[x * bpp:(x + 1) * bpp]
            px.append(tuple(p) if bpp == 4 else (p[0], p[1], p[2], 255))
    return w, h, px


def write(w, h, px):
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        for x in range(w):
            raw.extend(px[y * w + x])

    def chunk(t, b):
        return struct.pack(">I", len(b)) + t + b + struct.pack(">I", zlib.crc32(t + b) & 0xFFFFFFFF)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b""))


def size(data):
    return struct.unpack(">II", data[16:24])


def storm_ghast(w, h, px):
    """Vanilla ghast (64x32) -> storm-slate body, glowing cyan eyes/mouth, ruby gem on the forehead
    of the front face. Returned on a 64x64 canvas (item models want square textures)."""
    out = []
    for r, g, b, a in px:
        if a == 0:
            out.append((0, 0, 0, 0))
            continue
        hh, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if v > 0.7:                                  # pale skin -> dark storm slate, keep the shading
            nh, ns, nv = 0.6, 0.3, 0.22 + (v - 0.7) * 0.9
        else:                                        # dark marks (eyes, mouth, underside) -> glowing cyan
            nh, ns, nv = 0.5, 0.65, 0.95
        nr, ng, nb = colorsys.hsv_to_rgb(nh, ns, nv)
        out.append((round(nr * 255), round(ng * 255), round(nb * 255), a))
    ruby = {  # front face is x 16..31, y 16..31; gem centred, rows 17..20
        (23, 17): (150, 0, 20), (24, 17): (200, 10, 40),
        (22, 18): (150, 0, 20), (23, 18): (255, 170, 180), (24, 18): (255, 40, 60), (25, 18): (170, 0, 25),
        (22, 19): (170, 0, 25), (23, 19): (255, 40, 60), (24, 19): (230, 20, 50), (25, 19): (150, 0, 20),
        (23, 20): (150, 0, 20), (24, 20): (170, 0, 25),
    }
    for (x, y), (r, g, b) in ruby.items():
        out[y * w + x] = (r, g, b, 255)
    canvas = [(0, 0, 0, 0)] * (64 * 64)
    for y in range(h):
        for x in range(w):
            canvas[y * 64 + x] = out[y * w + x]
    return 64, 64, canvas


def void_recolor(px):
    """Blue/cyan cloth -> deep void purple, grey skin -> ashen violet, bright pale pixels (eyes, trims)
    -> glowing magenta."""
    out = []
    for r, g, b, a in px:
        if a == 0:
            out.append((r, g, b, a))
            continue
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if s > 0.25 and 0.45 <= h <= 0.75:          # blues and cyans: the robe
            h, s, v = 0.78, min(1.0, s * 1.2 + 0.1), v * 0.75
        elif s <= 0.25 and v > 0.85:                 # very bright, unsaturated: eyes / highlights
            h, s, v = 0.85, 0.75, 1.0
        elif s <= 0.25:                              # greys: skin and shading
            h, s, v = 0.76, 0.22, v * 0.7
        else:                                        # anything else: pull toward the palette
            h, s, v = (h * 0.4 + 0.8 * 0.6) % 1.0, s * 0.9, v * 0.85
        nr, ng, nb = colorsys.hsv_to_rgb(h, s, v)
        out.append((round(nr * 255), round(ng * 255), round(nb * 255), a))
    return out
