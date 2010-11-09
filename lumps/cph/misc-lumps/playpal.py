#!/usr/bin/env python
# Script to generate the PLAYPAL lump used by the Doom engine, specifically the
# which contains 14 alternative palettes which are used for various
# environmental effects. The base palette from which these are derived is either
# generated, or taken from a file.
#
# This is a Python version of the original Perl script.
#
# Copyright (C) 2008  Simon Howard
# Copyright (C) 2001  Colin Phipps <cphipps@doomworld.com>
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

import os
import sys
import struct

# IHS (Intensity Hue Saturation) to RGB conversion, utility function
#
# Obtained from a web page, which credited the following for the algorithm
#  Kruse, F.A. and G.L. Raines, 1984. "A Technique For Enhancing Digital
#  Colour Images by Contrast Stretching in Munsell Colour Space",
#  Proceedings of the International Symposium on Remote Sensing of
#  Environment, 3rd Thematic Conference, Environmental Research Institute
#  of Michigan, Colorado Springs, Colorado, pp. 755-773.
#  Bonham-Carter, Graeme F., 1994.  Geographic Informations Systems for
#  Geoscientists: Modelling with GIS. Computer Methods in the
#  Geosciences, Volume 13, published by Pergamon (Elsevier Science Ltd),
#  pp. 120-125.

R2 = 1.0 / 2
R3 = 1.0 / 3
R6 = 1.0 / 6
PI = 3.141592

def ihs_to_rgb(i, h, s):
	i = (i * 422) / 255
	h = (h * 2 * PI) / 255
	s = (s * 208.2066) / 255

	b, x = s * math.cos(h), s * math.sin(h)

	return (R3 * i - R6 * b - R2 * x,
		R3 * i - R6 * b + R2 * x,
		R3 * i + R6 * 2 * b)

# New palette builder

def make_pal_range(i, h, s, n):

	map_function = lambda x: ihs_to_rgb(i * (n - x) / n,
	                                    h,
	                                    s * (n - x) / n),

	return map(map_function, range(n))

# Very crude traversal of the IHS colour ball

def make_palette_new():
	result = []
	
	result += make_pal_range(255, 0, 0, 32)

	for i in range(7):
		result += make_pal_range(127, 171 + (i + 1) * 256 / 7, 255, 16)
	
	for i in range(7):
		result += make_pal_range(256, (i + 1) * 256 / 7, 127, 16)

# Return palette read from named file

def read_palette(filename):
	f = open(filename, "rb")

	colors = []

	for i in range(256):
		data = f.read(3)
		color = struct.unpack("BBB", data)

		colors.append(color)

	f.close()

	return colors

def make_palette(filename):
	if filename is None:
		return make_palette_new
	else:
		return read_palette(filename)

# Old palette builder
#sub make_pal_range($$$$$$)
#{
#  my ($rs,$gs,$bs,$re,$ge,$be) = @_;
#  return map { my $e = $_/16; my $s = 1-$e;
#  [$rs*$s + $re*$e, $gs*$s + $ge*$e, $bs*$s + $be * $e] } (1..16);
#}
#
#sub make_palette ()
#{
#  my @p = (
#  make_pal_range(0,0,0,0,0,0), # hmmm
#  make_pal_range(255,255,255,255,0,0), # pinks
#  make_pal_range(255,0,0,0,0,0), # dull reds
#  make_pal_range(255,128,255,192,192,0), # yellows
#  make_pal_range(255,255,0,0,0,0), # yellows
#  make_pal_range(255,255,255,0,0,0), # white
#  make_pal_range(127,127,127,0,0,0), # gray
#  make_pal_range(255,255,255,0,255,0), # light greens
#  make_pal_range(0,255,0,0,0,0), # greens
#  make_pal_range(0,0,0,0,0,0), # hmmm
#  make_pal_range(0,0,255,0,0,0), # dark blues
#  make_pal_range(255,255,255,0,0,255), # bright blues
#  make_pal_range(255,0,255,0,0,0), # magenta
#  make_pal_range(0,255,255,0,0,0), # cyan
#  make_pal_range(0,0,0,0,0,0), # hmmm
#  make_pal_range(0,0,0,0,0,0)); # hmmm
#  return \@p;
#}

# Now the PLAYPAL stuff - take the main palette and construct biased versions
# for the palette translation stuff

# Bias an entire palette

def bias_palette_towards(palette, target, p):

	def bias_rgb(rgb):
		r = []

		for i in range(3):
			r.append(rgb[i] * (1 - p) + target[i] * p)

		return r

	return map(bias_rgb, palette)

# Encode palette in the 3-byte RGB triples format expected by the engine

def clamp_pixval(v):
	if v < 0:
		return 0
	elif v > 255:
		return 255
	else:
		return int(v)

def output_palette(pal):

	for color in palette:
		color = tuple(map(clamp_pixval, color))
		
		encoded = struct.pack("BBB", *color)
		os.write(sys.stdout.fileno(), encoded)

# Main program - make a base palette, then do the biased versions

if len(sys.argv) < 2:
	print("Usage: %s <base filename> > playpal.lmp" % sys.argv[0])
	sys.exit(1)

base_pal = read_palette(sys.argv[1])

# From st_stuff.c, Copyright 1999 id Software, license GPL
#define STARTREDPALS         1
#define STARTBONUSPALS       9
#define NUMREDPALS           8
#define NUMBONUSPALS         4
#define RADIATIONPAL         13

palettes = []

# Normal palette

palettes.append(base_pal)

# STARTREDPALS

for i in range(8):
	p = (i + 1) / 8.0

	palettes.append(bias_palette_towards(base_pal, (255, 0, 0), p))

# STARTBONUSPALS

for i in range(4):
	p = (i + 1) * 0.4 / 4

	palettes.append(bias_palette_towards(base_pal, (128, 128, 128), p))

# RADIATIONPAL

palettes.append(bias_palette_towards(base_pal, (0, 255, 0), 0.2))

for palette in palettes:
	output_palette(palette)

