#!/usr/bin/env python

from __future__ import print_function
import sys
import struct


def read():
    try:
        return sys.stdin.buffer.read()
    except AttributeError:
        return sys.stdin.read()


def write(out):
    try:
        sys.stdout.buffer.write(out)
    except AttributeError:
        sys.stdout.write(out)


def main():
    # read PLAYPAL from stdin, write minimal doom2.wad to stdout
    if sys.stdin.isatty():
        print(
            "Usage: %s < playpal.lmp > doom2.wad" % sys.argv[0],
            file=sys.stderr,
        )
        sys.exit(1)

    # three lumps needed - see bootstrap/README.txt
    lumps = [
        (b"PLAYPAL", read()),
        (b"TEXTURE1", struct.pack("i", 0)),  # empty texture1
        (b"PNAMES", struct.pack("i8s", 1, b"")),
    ]  # single pname

    # calculate wad directory (lump offsets etc.)
    pos = 12
    waddir = []
    for name, data in lumps:
        waddir.append((pos, len(data), name))
        pos += len(data)

    # write wad header
    write(struct.pack("4sii", b"IWAD", len(waddir), pos))

    # write lump contents
    for name, data in lumps:
        write(data)

    # write wad directory
    for i in waddir:
        write(struct.pack("ii8s", *i))


if __name__ == "__main__":
    main()
