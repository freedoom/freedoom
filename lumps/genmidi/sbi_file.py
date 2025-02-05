#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause
#
# Module to load Creative SBI OPL instrument files.
#

import struct
import sys

HEADER_VALUE = "SBI\x1a"

FIELDS = [
    "m_am_vibrato_eg",
    "c_am_vibrato_eg",
    "m_ksl_volume",
    "c_ksl_volume",
    "m_attack_decay",
    "c_attack_decay",
    "m_sustain_release",
    "c_sustain_release",
    "m_waveform",
    "c_waveform",
    "feedback_fm",
]


def read(filename):
    with open(filename, "rb") as f:
        data = f.read()

    header, name = struct.unpack("4s32s", data[0:36])
    header = header.decode("ascii")

    if header != HEADER_VALUE:
        raise Exception("Invalid header for SBI file!")

    instr_data = data[36:]
    result = {"name": name.decode("ascii").rstrip("\0").rstrip()}

    for i in range(len(FIELDS)):
        result[FIELDS[i]], = struct.unpack("B", instr_data[i : i + 1])

    return result


def write(filename, data):
    with open(filename, "wb") as f:
        f.write(struct.pack("4s", HEADER_VALUE.encode("ascii")))
        f.write(struct.pack("32s", data["name"].encode("ascii")))

        for field in FIELDS:
            f.write(struct.pack("B", data[field]))
        for x in range(16 - len(FIELDS)):
            f.write(struct.pack("B", 0))


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        print(filename)
        print(read(filename))
