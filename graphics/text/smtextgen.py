#!/usr/bin/env python
# SPDX-License-Identifier: BSD-3-Clause
#
# Script to generate text graphics using the "small" (HUD) font.
#

from PIL import Image
from glob import glob
import sys
import re

from image_dimensions import *
from tint import image_tint

# Background color for output files.
BACKGROUND_COLOR = None

# Width of a space character in pixels.
SPACE_WIDTH = 4

# Height of the font.
FONT_HEIGHT = 8

# Regexp to match dimensions/x,y coordinate pair.
DIMENSION_MATCH_RE = re.compile(r'(\d+)[x,](\d+)')

class Font(object):
	def __init__(self):
		self.get_font_widths()

	def compile_kerning_table(self, kerning_table):
		"""Given a dictionary of kerning patterns, compile Regexps."""

		result = {}
		for pattern, adjust in kerning_table.items():
			result[re.compile(pattern)] = adjust
		return result

	def get_font_widths(self):
		charfiles = glob('../stcfn*.png')
		self.char_widths = {}
		for c in range(128):
			filename = self.char_filename(chr(c))
			if filename not in charfiles:
				continue
			w, _ = get_image_dimensions(filename)
			self.char_widths[chr(c)] = w

	def __contains__(self, c):
		return c in self.char_widths

	def char_width(self, c):
		return self.char_widths[c]

	def char_filename(self, c):
		return '../stcfn%03d.png' % (ord(c))

	def draw_for_text(self, image, text, x, y):
		text = text.upper()

		x1, y1 = x, y

		for c in text:
			if c == '\n':
				y1 += FONT_HEIGHT
				x1 = x
			elif c == ' ':
				x1 += SPACE_WIDTH

			if c not in self:
				continue

			filename = self.char_filename(c)
			char_image = Image.open(filename)
			image.paste(char_image, (x1, y1))
			x1 += self.char_width(c)

def parse_command_line(args):
	if len(args) < 4 or (len(args) % 2) != 0:
		return None

	result = {
		'filename': args[0],
		'background': None,
		'strings': [],
	}

	m = DIMENSION_MATCH_RE.match(args[1])
	if not m:
		return None
	result['dimensions'] = (int(m.group(1)), int(m.group(2)))

	i = 2
	while i < len(args):
		if args[i] == '-background':
			result['background'] = args[i+1]
			i += 2
			continue

		m = DIMENSION_MATCH_RE.match(args[i])
		if not m:
			return None

		xy = (int(m.group(1)), int(m.group(2)))

		result['strings'].append((xy, args[i + 1]))
		i += 2

	return result

if __name__ == '__main__':

	args = parse_command_line(sys.argv[1:])

	if not args:
		print("Usage: smtextgen <filename> <size> [...text commands...]")
		print("Where each text command looks like:")
		print("  [x,y] [text]")
		sys.exit(0)

	smallfont = Font()

	if args['background'] is not None:
		background_image = Image.open(args['background'])
		background_image.load()
		background_image = background_image.convert("RGBA")

	image = Image.new("RGBA", args['dimensions'],(0,0,0,0))

	for xy, string in args['strings']:
		# Allow contents of a file to be included with special prefix:
		if string.startswith('include:'):
			with open(string[8:]) as f:
				string = f.read()

		# Allow special notation to indicate an image file to just draw
		# rather than rendering a string.
		if string.startswith('file:'):
			src_image = Image.open(string[5:])
			src_image.load()
			image.paste(src_image, (xy[0], xy[1]))
		else:
			smallfont.draw_for_text(image, string, xy[0], xy[1])

	if args['background'] is not None:
		image = Image.alpha_composite(background_image, image)

	image.save(args['filename'])

