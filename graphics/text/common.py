
import re
import subprocess
import sys

# ImageMagick commands used by this script:
CONVERT_COMMAND = 'convert'
IDENTIFY_COMMAND = 'identify'

# Output from 'identify' looks like this:
#  fontchars/font033.gif GIF 9x16 9x16+0+0 8-bit sRGB 32c 194B 0.000u 0:00.000
IDENTIFY_OUTPUT_RE = re.compile(r'(\S+)\s(\S+)\s(\d+)x(\d+)(\+\d+\+\d+)?\s')

# Regexp to identify strings that are all lowercase (can use shorter height)
LOWERCASE_RE = re.compile(r'^[a-z\!\. ]*$')

def get_image_dimensions(filename):
	proc = subprocess.Popen([IDENTIFY_COMMAND, filename],
	                        stdout=subprocess.PIPE)
	proc.wait()

	line = proc.stdout.readline().decode('utf-8')
	match = IDENTIFY_OUTPUT_RE.match(line)
	assert match is not None
	return (int(match.group(3)), int(match.group(4)))

def invoke_command(command):
	"""Invoke a command, printing the command to stdout.

	Args:
	  command: Command and arguments as a list.
	"""
	for arg in command:
		if arg.startswith('-'):
			sys.stdout.write("\\\n    ")

		if ' ' in arg or '#' in arg:
			sys.stdout.write(repr(arg))
		else:
			sys.stdout.write(arg)

		sys.stdout.write(' ')

	sys.stdout.write('\n')
	return subprocess.call(command)

