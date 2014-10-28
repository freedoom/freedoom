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
	"feedback_fm"
]

def read(filename):
	with open(filename, "rb") as f:
		data = f.read()

	header, name = struct.unpack("4s32s", data[0:36])
	header = header.decode("ascii")

	if header != HEADER_VALUE:
		raise Exception("Invalid header for SBI file!")

	instr_data = data[36:]
	result = { "name": name.decode("ascii").rstrip("\0") }

	for i in range(len(FIELDS)):
		result[FIELDS[i]], = struct.unpack("B", instr_data[i:i+1])

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

