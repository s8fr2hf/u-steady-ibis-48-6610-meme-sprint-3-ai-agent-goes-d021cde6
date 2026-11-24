#!/usr/bin/env python3
"""Meme Sprint 3 entrypoint (pure standard library).

Copies the already-committed entry.png to $MAKEFUN_OUTPUT_DIR/entry.png
and validates it against the gate: a whole PNG, at most 1 MiB,
1024 by 1024 pixels. The grader sandbox is stdlib-only, so this file
imports nothing beyond the standard library.
"""
import hashlib
import os
import shutil
import struct
import sys

MAX_BYTES = 1048576
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def fail(message):
    print("error: " + message, file=sys.stderr)
    sys.exit(1)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dest = os.path.join(out_dir, "entry.png")

    if not os.path.isfile(source):
        fail("entry.png not found next to main.py")
    size = os.path.getsize(source)
    if size > MAX_BYTES:
        fail("entry.png is %d bytes, over the 1 MiB limit" % size)

    with open(source, "rb") as handle:
        header = handle.read(33)
    if len(header) < 33 or header[:8] != b"\x89PNG\r\n\x1a\n":
        fail("entry.png is not a PNG file")
    width, height = struct.unpack(">II", header[16:24])
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        fail("entry.png is %dx%d, expected 1024x1024" % (width, height))

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, dest)
    os.chmod(dest, 0o644)

    # Verify the copy itself: a partial or corrupted copy must never
    # pass silently. Re-read the destination and compare its digest
    # with the source, then re-check its PNG header and dimensions.
    def digest(path):
        hasher = hashlib.sha256()
        with open(path, "rb") as handle:
            for chunk in iter(lambda: handle.read(65536), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    if digest(source) != digest(dest):
        fail("copied entry.png does not match the source")
    with open(dest, "rb") as handle:
        copied = handle.read(33)
    if len(copied) < 33 or copied[:8] != b"\x89PNG\r\n\x1a\n":
        fail("copied entry.png is not a PNG file")
    width, height = struct.unpack(">II", copied[16:24])
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        fail("copied entry.png is %dx%d, expected 1024x1024" % (width, height))
    print("verified copy sha256 %s" % digest(dest))
    print("wrote %s (%d bytes, 1024x1024)" % (dest, size))


if __name__ == "__main__":
    main()
