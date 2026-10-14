"""Builds a genuinely silent Ogg Vorbis file without any audio library.

Vorbis needs three header packets (identification, comment, setup/codebooks). These are copied from an
existing small .ogg; they contain codec settings, no audio. Every audio packet is then the single byte 0x00:
packet type 0 (audio), mode 0, window flags 0 (if any) and floor "unused" for every channel, which the
Vorbis spec decodes as a silent block with no residue.
"""

import struct

_CRC = []
for _i in range(256):
    _r = _i << 24
    for _ in range(8):
        _r = ((_r << 1) ^ 0x04C11DB7) if _r & 0x80000000 else (_r << 1)
    _CRC.append(_r & 0xFFFFFFFF)


def _crc(data):
    c = 0
    for b in data:
        c = ((c << 8) & 0xFFFFFFFF) ^ _CRC[((c >> 24) & 0xFF) ^ b]
    return c


def read_packets(data):
    """Returns (serial, packets) of the first logical stream."""
    pos, packets, cur, serial = 0, [], b"", None
    while pos < len(data):
        if data[pos:pos + 4] != b"OggS":
            raise ValueError("not an Ogg stream")
        nseg = data[pos + 26]
        serial = serial if serial is not None else struct.unpack("<I", data[pos + 14:pos + 18])[0]
        lacing = data[pos + 27:pos + 27 + nseg]
        body = pos + 27 + nseg
        for lv in lacing:
            cur += data[body:body + lv]
            body += lv
            if lv < 255:
                packets.append(cur)
                cur = b""
        pos = body
    return serial, packets


def _page(serial, seq, granule, packets, flags):
    lacing, body = bytearray(), b""
    for p in packets:
        n = len(p)
        while n >= 255:
            lacing.append(255)
            n -= 255
        lacing.append(n)
        body += p
    hdr = struct.pack("<4sBBqIIIB", b"OggS", 0, flags, granule, serial, seq, 0, len(lacing)) + bytes(lacing)
    page = bytearray(hdr + body)
    struct.pack_into("<I", page, 22, _crc(bytes(page)))
    return bytes(page)


def silent_ogg(template, seconds=2.0):
    serial, packets = read_packets(template)
    ident, comment, setup = packets[0], packets[1], packets[2]
    if ident[0] != 1 or ident[1:7] != b"vorbis":
        raise ValueError("template is not Vorbis")
    rate = struct.unpack("<I", ident[12:16])[0]
    bs0 = 1 << (ident[28] & 0x0F)            # short block size
    per_packet = bs0 // 2
    count = max(4, int(seconds * rate / per_packet) + 1)
    out = [_page(serial, 0, 0, [ident], 0x02), _page(serial, 1, 0, [comment, setup], 0)]
    seq, done, granule = 2, 0, 0
    while done < count:
        n = min(200, count - done)
        done += n
        granule = (done - 1) * per_packet      # the first audio packet only primes the decoder
        out.append(_page(serial, seq, granule, [b"\x00"] * n, 0x04 if done >= count else 0))
        seq += 1
    return b"".join(out), {"rate": rate, "short_block": bs0, "packets": count, "samples": granule}
