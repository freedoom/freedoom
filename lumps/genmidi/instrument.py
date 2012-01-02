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
	def __init__(self, file1, file2=None, note=None):
		self.instr1 = load_instrument(file1)

		if file2 is not None:
			self.instr2 = load_instrument(file2)
		else:
			self.instr2 = None

		self.fixed_note = note

NullInstrument = Instrument("dummy.sbi")

if __name__ == "__main__":
	for filename in sys.argv[1:]:
		Instrument(filename)

