#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause
#
# Module for interacting with Doom GENMIDI lumps.
#

from instrument import Instrument, NullInstrument
import struct
import sys

GENMIDI_HEADER = "#OPL_II#"
NUM_INSTRUMENTS = 175
INSTR_DATA_LEN = 36
INSTR_NAME_LEN = 32

FLAG_FIXED_PITCH = 0x0001
FLAG_TWO_VOICE = 0x0004

KSL_MASK = 0xC0
VOLUME_MASK = 0x3F

# Order of fields in GENMIDI data structures.

GENMIDI_FIELDS = [
    "m_am_vibrato_eg",
    "m_attack_decay",
    "m_sustain_release",
    "m_waveform",
    "m_ksl",
    "m_volume",
    "feedback_fm",
    "c_am_vibrato_eg",
    "c_attack_decay",
    "c_sustain_release",
    "c_waveform",
    "c_ksl",
    "c_volume",
    "null",
    "note_offset",
]

# Encode a single voice of an instrument to binary.


def encode_voice(data, offset):
    result = dict(data)

    result["m_ksl"] = data["m_ksl_volume"] & KSL_MASK
    result["m_volume"] = data["m_ksl_volume"] & VOLUME_MASK
    result["c_ksl"] = data["c_ksl_volume"] & KSL_MASK
    result["c_volume"] = data["c_ksl_volume"] & VOLUME_MASK

    result["null"] = 0
    result["note_offset"] = offset

    return struct.pack(
        "<BBBBBBBBBBBBBBh", *map(lambda key: result[key], GENMIDI_FIELDS)
    )


# Encode an instrument to binary.


def encode_instrument(instrument):
    flags = 0

    instr1_data = encode_voice(instrument.voice1, instrument.offset1)

    if instrument.voice2 is not None:
        flags |= FLAG_TWO_VOICE
        instr2_data = encode_voice(instrument.voice2, instrument.offset2)
    else:
        instr2_data = encode_voice(NullInstrument.voice1, 0)

    if instrument.fixed_note is not None:
        flags |= FLAG_FIXED_PITCH
        fixed_note = instrument.fixed_note
    else:
        fixed_note = 0

    header = struct.pack("<hBB", flags, 128 + instrument.tune, fixed_note)

    return header + instr1_data + instr2_data


def encode_instruments(instruments):
    result = []

    for instrument in instruments:
        result.append(encode_instrument(instrument))

    return b"".join(result)


def encode_instrument_names(instruments):
    result = []

    for instrument in instruments:
        instr_name = instrument.voice1["name"].encode("ascii")
        result.append(struct.pack("32s", instr_name))

    return b"".join(result)


def write(filename, instruments):
    header = struct.pack(
        "%is" % len(GENMIDI_HEADER), GENMIDI_HEADER.encode("ascii")
    )

    with open(filename, "wb") as f:
        f.write(header)
        f.write(encode_instruments(instruments))
        f.write(encode_instrument_names(instruments))


def decode_voice(data, name):

    fields = struct.unpack("<BBBBBBBBBBBBBBh", data)

    result = {}
    for i in range(len(GENMIDI_FIELDS)):
        result[GENMIDI_FIELDS[i]] = fields[i]

    result["m_ksl_volume"] = result["m_ksl"] | result["m_volume"]
    result["c_ksl_volume"] = result["c_ksl"] | result["c_volume"]
    result["name"] = name.decode("ascii").rstrip("\0").rstrip()

    return result


def decode_instrument(data, name):
    flags, finetune, fixed_note = struct.unpack("<hBB", data[0:4])

    voice1 = decode_voice(data[4:20], name)
    offset1 = voice1["note_offset"]

    # Second voice?

    if (flags & FLAG_TWO_VOICE) != 0:
        voice2 = decode_voice(data[20:], name)
        offset2 = voice2["note_offset"]
    else:
        voice2 = None
        offset2 = 0

    # Null out fixed_note if the fixed pitch flag isn't set:

    if (flags & FLAG_FIXED_PITCH) == 0:
        fixed_note = None

    return Instrument(
        voice1, voice2, off1=offset1, off2=offset2, note=fixed_note,
        tune=finetune - 128
    )


def read(filename):
    with open(filename, "rb") as f:
        data = f.read()

    # Check header:

    header = data[0 : len(GENMIDI_HEADER)]
    if header.decode("ascii") != GENMIDI_HEADER:
        raise Exception("Incorrect header for GENMIDI lump")

    body = data[len(GENMIDI_HEADER) :]
    instr_data = body[0 : NUM_INSTRUMENTS * INSTR_DATA_LEN]
    instr_names = body[NUM_INSTRUMENTS * INSTR_DATA_LEN :]
    result = []

    for i in range(NUM_INSTRUMENTS):
        data = instr_data[i * INSTR_DATA_LEN : (i + 1) * INSTR_DATA_LEN]
        name = instr_names[i * INSTR_NAME_LEN : (i + 1) * INSTR_NAME_LEN]

        result.append(decode_instrument(data, name))

    return result


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        instruments = read(filename)
        for i in range(len(instruments)):
            instrument = instruments[i]
            fixed_note = instrument.fixed_note

            if fixed_note is not None:
                print("%i (fixed note: %i):" % (i, fixed_note))
            else:
                print("%i:" % i)

            print("\tVoice 1: %s" % instrument.voice1)
            if instrument.voice2 is not None:
                print("\tVoice 2: %s" % instrument.voice2)
