#!/usr/bin/env python
#
# Copyright (C) 2001 Colin Phipps <cphipps@doomworld.com>
# Copyright (C) 2008, 2013 Simon Howard
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
#
#
# Takes PLAYPAL as input (filename is the only parameter)
# Produces a light graduated COLORMAP on stdout
# O(n^2)
#
# This was originally a Perl script by Colin Phipps; it was converted
# to Python and now is a more generic tool for generating all kinds of
# COLORMAP effects.
#

import os
import sys
import struct

# Parameters affecting colormap generation:

# "Darkness" is this color, which is usually black, but can be
# overridden (RGB 0-255):
dark_color = (0, 0, 0)

# Color to tint the colormap (RGB 0.0-1.0):
tint_color = (255, 255, 255)

# Fractional balance between tint and normal color. 0 is no tint applied,
# 1.0 is full tint.
tint_frac = 0

# Fudge factor to adjust brightness when calculating 'tinted' version
# of colors. Larger values are brighter but may cause color clipping.
# A value of 0.33 is a straight-average of the RGB channels. Maximum
# sensible value is 1.0, though it can be overdriven for fancy
# brightness effects.
tint_bright = 0.5

def read_palette(filename):
	"""Read palette from file and return a list of tuples containing
	   RGB values."""
	f = open(filename, "rb")

	colors = []

	for i in range(256):
		data = f.read(3)

		color = struct.unpack("BBB", data)
		colors.append(color)

	return colors

# Return closest palette entry to the given RGB triple

def search_palette(palette, target):
	"""Search the given palette and find the nearest matching
	   color to the given color, returning an index into the
	   palette of the color that best matches."""
	best_diff = None
	best_index = None

	def square(x):
		return x * x

	for i in range(len(palette)):
		color = palette[i]

		diff = square(target[0] - color[0])            \
		     + square(target[1] - color[1])            \
		     + square(target[2] - color[2])

		if best_index is None or diff < best_diff:
			best_diff = diff
			best_index = i

	return best_index

def generate_colormap(colors, palette):
	"""Given a list of colors, translate these into indexes into
	   the given palette, finding the nearest color where an exact
	   match cannot be found."""
	result = []

	for color in colors:
		index = search_palette(palette, color)
		result.append(index)

	return result

def tint_colors(colors, tint, bright=0.5):
	"""Given a list of colors, tint them a particular color."""

	result = []
	for c in colors:
		# I've experimented with different methods of calculating
		# intensity, but this seems to work the best. This is basically
		# doing an average of the full channels, but a straight
		# average causes the picture to get darker - eg. (0,0,255)
		# maps to (87,87,87). So we have a controllable brightness
		# factor that allows the brightness to be adjusted.
		intensity = min((c[0] + c[1] + c[2]) * bright, 255) / 255.0
		result.append((
			tint[0] * intensity,
			tint[1] * intensity,
			tint[2] * intensity,
		))

	return result

def blend_colors(colors1, colors2, factor=0.5):
	"""Blend the two given lists of colors, with 'factor' controlling
	   the mix between the two. factor=0 is exactly colors1, while
	   factor=1 is exactly colors2. Returns a list of blended colors."""
	result = []

	for index, c1 in enumerate(colors1):
		c2 = colors2[index]

		result.append((
			c2[0] * factor + c1[0] * (1 - factor),
			c2[1] * factor + c1[1] * (1 - factor),
			c2[2] * factor + c1[2] * (1 - factor),
		))

	return result

def invert_colors(colors):
	"""Given a list of colors, translate them to inverted monochrome."""
	result = []

	for color in colors:
		average = (color[0] + color[1] + color[2]) // 3
		inverse = 255 - average

		result.append((inverse, inverse, inverse))

	return result

def solid_color_list(color):
	"""Generate a 256-entry palette where all entries are the
	   same color."""
	return [color] * 256

def output_colormap(colormap):
	"""Output the given palette to stdout."""
	for c in colormap:
		x = struct.pack("B", c)
		os.write(sys.stdout.fileno(), x)

def print_palette(colors):
	for y in range(16):
		for x in range(16):
			color = colors[y * 16 + x]

			print("#%02x%02x%02x" % color)

		print()

def parse_color_code(s):
	"""Parse a color code in HTML color code format, into an RGB
	   3-tuple value."""
	if not s.startswith('#') or len(s) != 7:
		raise Exception('Not in HTML color code form: %s' % s)
	return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16))

def set_parameter(name, value):
	"""Set configuration value, from command line parameters."""
	global dark_color, tint_color, tint_frac, tint_bright

	if name == 'dark_color':
		dark_color = parse_color_code(value)
	elif name == 'tint_color':
		tint_color = parse_color_code(value)
	elif name == 'tint_pct':
		tint_frac = int(value) / 100.0
	elif name == 'tint_bright':
		tint_bright = float(value)
	else:
		raise Exception("Unknown parameter: '%s'" % name)

# Parse command line.

playpal_filename = None

for arg in sys.argv[1:]:
	if arg.startswith('--') and '=' in arg:
		key, val = arg[2:].split('=', 2)
		set_parameter(key, val)
	else:
		playpal_filename = arg

if playpal_filename is None:
	print("Usage: %s playpal.lmp > output-file.lmp" % sys.argv[0])
	sys.exit(1)

palette = read_palette(playpal_filename)
colors = palette

# Apply tint, if enabled.
# The tint is intentionally applied *before* the darkening effect is
# applied. This allows us to darken to a different color than the tint
# color, if so desired.
if tint_frac > 0:
	colors = blend_colors(palette,
	                      tint_colors(colors, tint_color, tint_bright),
	                      tint_frac)

# Generate colormaps for different darkness levels, by blending between
# the default colors and a palette where every entry is the "dark" color.
dark = solid_color_list(dark_color)

for i in range(32):
	darken_factor = (32 - i) / 32.0
	darkened_colors = blend_colors(dark, colors, darken_factor)
	output_colormap(generate_colormap(darkened_colors, palette))

# Inverse color map for invulnerability effect.
inverse_colors = invert_colors(palette)
output_colormap(generate_colormap(inverse_colors, palette))

# Last colormap is all black, and is actually unused in Vanilla Doom
# (it was mistakenly included by the dcolors.c utility). It's
# strictly unneeded, though some utilities (SLADE) do not detect a
# lump as a COLORMAP unless it is the right length.
output_colormap(generate_colormap(dark, palette))

