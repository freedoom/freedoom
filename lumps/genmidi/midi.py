#!/usr/bin/env python
#
# Copyright (c) 2011, 2012
# Contributors to the Freedoom project.  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#  * Neither the name of the freedoom project nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
# OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# ----------------------------------------------------------------------
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
		self.C  = base
		self.Cs = base + 1
		self.Db = base + 1
		self.D  = base + 2
		self.Ds = base + 3
		self.Eb = base + 3
		self.E  = base + 4
		self.F  = base + 5
		self.Fs = base + 6
		self.Gb = base + 6
		self.G  = base + 7
		self.Gs = base + 8
		self.Ab = base + 8
		self.A  = base + 9
		self.As = base + 10
		self.Bb = base + 10
		self.B  = base + 11

On5 = Octave(0)      # Octave -5
On4 = Octave(12)     # Octave -4
On3 = Octave(24)     # Octave -3
On2 = Octave(36)     # Octave -2
On1 = Octave(48)     # Octave -1
O0  = Octave(60)     # Octave 0
O1  = Octave(72)     # Octave 1
O2  = Octave(84)     # Octave 2
O3  = Octave(96)     # Octave 3
O4  = Octave(108)    # Octave 4
O5  = Octave(120)    # Octave 5

# Given a MIDI note number, return a note definition in terms of the
# constants above.

def def_for_note(note):
	OCTAVES = [ "On5", "On4", "On3", "On2", "On1",
	            "O0", "O1", "O2", "O3", "O4", "O5" ]
	NOTES = [ "C", "Cs", "D", "Ds", "E", "F", "Fs",
	          "G", "Gs", "A", "As", "B" ]

	return "%s.%s" % (OCTAVES[note // 12], NOTES[note % 12])

