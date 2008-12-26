#!/usr/bin/env python
#
# Takes PLAYPAL as input (filename is the only parameter)
# Produces a light graduated COLORMAP on stdout
# O(n^2)
#
# This is a Python version of Colin's original Perl script.
#
# Copyright (C) 2001 Colin Phipps <cphipps@doomworld.com>
# Copyright (C) 2008 Simon Howard
# Parts copyright (C) 1999 by id Software (http://www.idsoftware.com/)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import sys

# Return palette read from named file

def read_palette(filename):
	f = file(filename)

	colors = []

	for i in range(256):
		color = f.read(3)

		colors.append((ord(color[0]), ord(color[1]), ord(color[2])))

	return colors

def square(x):
	return x * x

# Return closest palette entry to the given RGB triple

def search_palette(colors, target):
	best_diff = None
	best_index = None

	for i in range(len(colors)):
		color = colors[i]

		diff = square(target[0] - color[0])            \
		     + square(target[1] - color[1])            \
		     + square(target[2] - color[2])

		if best_index is None or diff < best_diff:
			best_diff = diff
			best_index = i

	return best_index

def generate_colormap(colors, transform_function):
	result = []

	for color in colors:
		transformed_color = transform_function(color)
		transformed_index = search_palette(colors, transformed_color)
		result.append(transformed_index)

	return result

def generate_darkened_colormap(colors, factor):

	darken_function = lambda c: ( c[0] * factor,         \
	                              c[1] * factor,         \
	                              c[2] * factor )

	return generate_colormap(colors, darken_function)

def output_colormap(colormap):
	for c in colormap:
		sys.stdout.write(chr(c))

def inverse_color(color):
	average = (color[0] + color[1] + color[2]) / 3
	inverse = 255 - average

	return (inverse, inverse, inverse)

def print_palette(colors):
	for y in range(16):
		for x in range(16):
			color = colors[y * 16 + x]

			print "#%02x%02x%02x" % color,

		print

if len(sys.argv) < 2:
	print "Usage: %s <base filename> > output-file.lmp"
	sys.exit(1)

colors = read_palette(sys.argv[1])

#print_palette(colors)
#sys.exit(0)

# Main color ranges

for i in range(32):
	darken_factor = (32 - i) / 32.0
	colormap = generate_darkened_colormap(colors, darken_factor)
	output_colormap(colormap)

# Print inverse color map

inverse_colormap = generate_colormap(colors, inverse_color)

output_colormap(inverse_colormap)

