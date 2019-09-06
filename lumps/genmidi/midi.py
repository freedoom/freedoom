#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause
#
# Constants for MIDI notes.
#
# For example:
#    F# in Octave 3:      O3.Fs
#    C# in Octave -2:     On2.Cs
#    D-flat in Octave 1:  O1.Db
#    D in Octave 0:       O0.D
#    E in Octave 2:       O2.E


class Octave:
    def __init__(self, base):
        self.C = base
        self.Cs = base + 1
        self.Db = base + 1
        self.D = base + 2
        self.Ds = base + 3
        self.Eb = base + 3
        self.E = base + 4
        self.F = base + 5
        self.Fs = base + 6
        self.Gb = base + 6
        self.G = base + 7
        self.Gs = base + 8
        self.Ab = base + 8
        self.A = base + 9
        self.As = base + 10
        self.Bb = base + 10
        self.B = base + 11


On5 = Octave(0)  # Octave -5
On4 = Octave(12)  # Octave -4
On3 = Octave(24)  # Octave -3
On2 = Octave(36)  # Octave -2
On1 = Octave(48)  # Octave -1
O0 = Octave(60)  # Octave 0
O1 = Octave(72)  # Octave 1
O2 = Octave(84)  # Octave 2
O3 = Octave(96)  # Octave 3
O4 = Octave(108)  # Octave 4
O5 = Octave(120)  # Octave 5

# Given a MIDI note number, return a note definition in terms of the
# constants above.


def def_for_note(note):
    OCTAVES = [
        "On5",
        "On4",
        "On3",
        "On2",
        "On1",
        "O0",
        "O1",
        "O2",
        "O3",
        "O4",
        "O5",
    ]
    NOTES = ["C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs", "A", "As", "B"]

    return "%s.%s" % (OCTAVES[note // 12], NOTES[note % 12])
