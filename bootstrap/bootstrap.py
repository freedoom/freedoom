#!/usr/bin/env python3

import sys
import struct

def main():
    # read PLAYPAL from stdin, write minimal doom2.wad to stdout
    if sys.stdin.isatty():
        print("Usage: %s < playpal.lmp > doom2.wad" % sys.argv[0],
                file=sys.stderr)
        sys.exit(1)

    # three lumps needed - see bootstrap/README.txt
    lumps = [(b'PLAYPAL',  sys.stdin.buffer.read()),
             (b'TEXTURE1', struct.pack("i", 0)), # empty texture1
             (b'PNAMES',   struct.pack("i8s", 1, b''))] # single pname

    # calculate wad directory (lump offsets etc.)
    pos = 12
    waddir = []
    for name, data in lumps:
        waddir.append((pos, len(data), name))
        pos += len(data)

    # write wad header
    wadheader = (b'IWAD', len(waddir), pos)
    sys.stdout.buffer.write(struct.pack("4sii", *wadheader))

    # write lump contents
    for name, data in lumps:
        sys.stdout.buffer.write(data)

    # write wad directory
    for i in waddir:
        sys.stdout.buffer.write(struct.pack("ii8s", *i))

if __name__ == "__main__": main()
