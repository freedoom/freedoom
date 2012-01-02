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
# Module to load OPL instrument files.
#

import os
import sys
import sbi_file
import a2i_file

# Check the specified instrument data is OPL2-compatible and does not
# use any OPL3 features. Returns an error message, or 'None' if data
# is valid.

def check_opl2(filename, data):
	def opl2_warning(message):
		print >> sys.stderr, "%s: %s" % (filename, message)

	# CHA,B control stereo, but are ignored on OPL2, so it's no problem:
	#if (data["feedback_fm"] & 0xf0) != 0:
	#	opl2_warning("Cannot use CHA,B,C,D: %02x" % data["feedback_fm"])

	if data["m_waveform"] > 3:
		opl2_warning("Modulator uses waveform %i: only 0-3 supported" %
		             data["m_waveform"])
	if data["c_waveform"] > 3:
		opl2_warning("Carrier uses waveform %i: only 0-3 supported" %
		             data["c_waveform"])

def load_instrument(filename):
	filename = os.path.join("instruments", filename)

	if filename.endswith(".a2i"):
		result = a2i_file.read(filename)
	elif filename.endswith(".sbi"):
		result = sbi_file.read(filename)
	else:
		raise Exception("Unknown instrument file type: '%s'" % filename)

	check_opl2(filename, result)

	return result

class Instrument:
	def __init__(self, file1, file2=None, off1=0, off2=0, note=None):
		self.instr1 = load_instrument(file1)

		if file2 is not None:
			self.instr2 = load_instrument(file2)
		else:
			self.instr2 = None

		self.fixed_note = note
		self.offset1 = off1
		self.offset2 = off2

NullInstrument = Instrument("dummy.sbi")

if __name__ == "__main__":
	for filename in sys.argv[1:]:
		Instrument(filename)

