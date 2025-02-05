#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause
#
# Module to load OPL instrument files.
#

import os
import sys
import sbi_file
import a2i_file

DO_OPL2_CHECK = False

# Check the specified instrument data is OPL2-compatible and does not
# use any OPL3 features. Returns an error message, or 'None' if data
# is valid.


def check_opl2(filename, data):
    def opl2_warning(message):
        print("%s: %s" % (filename, message), file=sys.stderr)

    # CHA,B control stereo, but are ignored on OPL2, so it's no problem:
    # if (data["feedback_fm"] & 0xf0) != 0:
    # 	opl2_warning("Cannot use CHA,B,C,D: %02x" % data["feedback_fm"])

    if data["m_waveform"] > 3:
        opl2_warning(
            "Modulator uses waveform %i: only 0-3 supported"
            % data["m_waveform"]
        )
    if data["c_waveform"] > 3:
        opl2_warning(
            "Carrier uses waveform %i: only 0-3 supported" % data["c_waveform"]
        )


def load_instrument(filename):

    # As a hack, a literal dictionary of the values can be specified
    # in place of a filename.

    if isinstance(filename, dict):
        return filename

    filename = os.path.join("instruments", filename)

    if filename.endswith(".a2i"):
        result = a2i_file.read(filename)
    elif filename.endswith(".sbi"):
        result = sbi_file.read(filename)
    else:
        raise Exception("Unknown instrument file type: '%s'" % filename)

    if DO_OPL2_CHECK:
        check_opl2(filename, result)

    return result


class Instrument:
    def __init__(self, file1, file2=None, off1=0, off2=0, note=None, tune=0):
        self.voice1 = load_instrument(file1)

        if file2 is not None:
            self.voice2 = load_instrument(file2)
        else:
            self.voice2 = None

        self.fixed_note = note
        self.offset1 = off1
        self.offset2 = off2
        self.tune = tune


NullInstrument = Instrument("dummy.sbi")

if __name__ == "__main__":
    for filename in sys.argv[1:]:
        Instrument(filename)
