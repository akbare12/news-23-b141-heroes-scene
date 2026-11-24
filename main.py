#!/usr/bin/env python3
"""news-23 b141 heroes-scene: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
which the grader points at an empty output dir while /bot stays read-only.
Validates the PNG by hand: signature, IHDR 1024x1024, chunk CRCs, IEND last.
"""
import hashlib
import os
import struct
import sys
import zlib

# Filled in after the final image is rendered (see revision below).
EXPECTED_SHA256 = "0996834bf1faff4626312abf36c6f90bef9d28b30215e2e19b64f6dd6cb4e410"
EXPECTED_SIZE = 191614


def fail(msg):
    print("main.py: error: " + msg, file=sys.stderr)
    sys.exit(1)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    if os.path.isfile(out_dir_abs):
        fail("MAKEFUN_OUTPUT_DIR is a file, not a directory: %s" % out_dir)
    if out_dir_abs == here or out_dir_abs.startswith(here + os.sep):
        fail("MAKEFUN_OUTPUT_DIR must not be inside the repo: %s" % out_dir)
    dst = os.path.join(out_dir_abs, "entry.png")
    if os.path.abspath(dst) == os.path.abspath(src):
        fail("output would overwrite the source image")

    try:
        with open(src, "rb") as f:
            data = f.read()
    except OSError as e:
        fail("cannot read %s: %s" % (src, e))

    # Size checks: at least 10_000 bytes, at most 1 MiB.
    if len(data) < 10000:
        fail("entry.png too small: %d bytes" % len(data))
    if len(data) > 1024 * 1024:
        fail("entry.png over 1 MiB: %d bytes" % len(data))
    if len(data) != EXPECTED_SIZE:
        fail("entry.png size %d != expected %d" % (len(data), EXPECTED_SIZE))

    # PNG signature.
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("bad PNG signature")

    # First chunk must be IHDR, 13 bytes, 1024x1024, bit depth 8,
    # colour type 2 (RGB) or 6 (RGBA), compression/filter/interlace 0.
    # Byte layout: 0-7 signature, 8-11 length, 12-15 type, 16-28 IHDR data,
    # 29-32 CRC (type+data only, NOT the length field), next chunk at 33.
    # The CRC covers bytes 12:29; including the length bytes 8:12 would
    # wrongly reject a valid file.
    if len(data) < 33:
        fail("file truncated before IHDR")
    ihdr_len = struct.unpack(">I", data[8:12])[0]
    ihdr_type = data[12:16]
    if ihdr_len != 13 or ihdr_type != b"IHDR":
        fail("first chunk is not a 13-byte IHDR")
    ihdr_crc_stored = struct.unpack(">I", data[29:33])[0]
    ihdr_crc = zlib.crc32(data[12:29]) & 0xFFFFFFFF
    if ihdr_crc != ihdr_crc_stored:
        fail("bad CRC in chunk IHDR")
    width, height, depth, ctype, comp, filt, inter = struct.unpack(
        ">IIBBBBB", data[16:29])
    if (width, height) != (1024, 1024):
        fail("IHDR is %dx%d, expected 1024x1024" % (width, height))
    if depth != 8 or ctype not in (2, 6):
        fail("IHDR bit depth %d / colour type %d unsupported" % (depth, ctype))
    if comp != 0 or filt != 0 or inter != 0:
        fail("IHDR compression/filter/interlace must all be 0")

    # Walk the remaining chunks: CRC each, IDAT payloads non-empty and
    # >= 1000 bytes total, IEND 0-byte must be the last chunk, no trailing data.
    pos = 33
    idat_total = 0
    saw_iend = False
    while True:
        if pos + 8 > len(data):
            fail("truncated chunk header at offset %d" % pos)
        clen = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        if pos + 12 + clen > len(data):
            fail("truncated chunk %r at offset %d" % (ctype, pos))
        crc_stored = struct.unpack(">I", data[pos + 8 + clen:pos + 12 + clen])[0]
        crc = zlib.crc32(data[pos + 4:pos + 8 + clen]) & 0xFFFFFFFF
        if crc != crc_stored:
            fail("bad CRC in chunk %r" % ctype)
        if ctype == b"IDAT":
            if clen == 0:
                fail("empty IDAT chunk")
            idat_total += clen
        if ctype == b"IEND":
            if clen != 0:
                fail("IEND must be 0 bytes")
            if pos + 12 + clen != len(data):
                fail("trailing data after IEND")
            saw_iend = True
            break
        pos += 12 + clen
    if not saw_iend:
        fail("no IEND chunk found")
    if idat_total < 1000:
        fail("IDAT payload too small: %d bytes" % idat_total)

    sha = hashlib.sha256(data).hexdigest()
    if sha != EXPECTED_SHA256:
        fail("sha256 %s != expected %s" % (sha, EXPECTED_SHA256))

    os.makedirs(out_dir_abs, exist_ok=True)
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        out = f.read()
    if out != data:
        fail("re-read output does not match source")
    print("wrote %s (%d bytes, sha256 %s)" % (dst, len(out), sha))


if __name__ == "__main__":
    main()
