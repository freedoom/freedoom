
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
	f = open(filename)
	data = f.read()
	f.close()

	header, name = struct.unpack("4s32s", data[0:36])

	if header != HEADER_VALUE:
		raise Exception("Invalid header for SBI file!")

	instr_data = data[36:]
	result = { "name": name.rstrip("\0") }

	for i in range(len(FIELDS)):
		result[FIELDS[i]], = struct.unpack("B", instr_data[i:i+1])

	return result

if __name__ == "__main__":
	for filename in sys.argv[1:]:
		print filename
		print read(filename)

