# SPDX-License-Identifier: BSD-3-Clause

import re
import subprocess
import sys

from PIL import Image

# Output from 'identify' looks like this:
#  fontchars/font033.png GIF 9x16 9x16+0+0 8-bit sRGB 32c 194B 0.000u 0:00.000
IDENTIFY_OUTPUT_RE = re.compile(r'(\S+)\s(\S+)\s(\d+)x(\d+)(\+\d+\+\d+)?\s')

# Regexp to identify strings that are all lowercase (can use shorter height)
LOWERCASE_RE = re.compile(r'^[a-z\!\. ]*$')


def get_image_dimensions(filename):
	"""Get image dimensions w x h

    Args:
      filename: filename of the image
    """
	with Image.open(filename) as img:
		width, height = img.size
	return (width, height)


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