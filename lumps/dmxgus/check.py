#!/usr/bin/env python
#
# Copyright (c) 2012
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
#
# Sanity check script for DMXGUS lump.
# Please run this script after making any changes to ultramid.ini.
#

import sys
import re

# These are the sizes (in bytes) of the patch files distributed
# with the GUS drivers. Having these means we can calculate the
# size in RAM (roughly) of the patch set for a given configuration
# and check it is within the limit.

GUS_PATCH_SIZES = {
	"acbass": 10829,    "accordn": 19623,   "acguitar": 52581,
	"acpiano": 65259,   "agogo": 27727,     "agogohi": 7283,
	"agogolo": 7283,    "altosax": 11711,   "applause": 60449,
	"atmosphr": 63035,  "aurora": 62503,    "bagpipes": 16057,
	"banjo": 64523,     "barisax": 21739,   "basslead": 53389,
	"bassoon": 16723,   "belltree": 64103,  "blank": 3367,
	"bongohi": 7233,    "bongolo": 9201,    "bottle": 25063,
	"bowglass": 49691,  "britepno": 72739,  "cabasa": 17203,
	"calliope": 46303,  "carillon": 12089,  "castinet": 12349,
	"celeste": 20207,   "cello": 18741,     "charang": 90661,
	"chiflead": 63381,  "choir": 45353,     "church": 4609,
	"claps": 11719,     "clarinet": 19161,  "clave": 5035,
	"clavinet": 3443,   "cleangtr": 46027,  "concrtna": 17981,
	"congahi1": 8753,   "congahi2": 9713,   "congalo": 9713,
	"contraba": 9723,   "cowbell": 6645,    "crystal": 60783,
	"cuica1": 18995,    "cuica2": 26017,    "cymbell": 34815,
	"cymchina": 48545,  "cymcrsh1": 63353,  "cymcrsh2": 62411,
	"cymride1": 35655,  "cymride2": 35655,  "cymsplsh": 63353,
	"distgtr": 38249,   "doo": 17333,       "echovox": 30287,
	"englhorn": 24675,  "epiano1": 15005,   "epiano2": 44191,
	"fantasia": 47229,  "fiddle": 12309,    "flute": 12383,
	"fngrbass": 19797,  "frenchrn": 28635,  "freshair": 58307,
	"fretless": 5605,   "fx-blow": 57693,   "fx-fret": 27631,
	"ghostie": 63301,   "glocken": 10695,   "gtrharm": 10173,
	"guiro1": 8561,     "guiro2": 18821,    "halopad": 60291,
	"harmonca": 15301,  "harp": 23927,      "helicptr": 50327,
	"highq": 3945,      "hihatcl": 9453,    "hihatop": 40417,
	"hihatpd": 3925,    "hitbrass": 63369,  "homeorg": 2301,
	"honky": 131905,    "hrpschrd": 7709,   "jazzgtr": 55923,
	"jingles": 34219,   "jungle": 27541,    "kalimba": 4739,
	"kick1": 9411,      "kick2": 10377,     "koto": 42079,
	"lead5th": 13233,   "maracas": 9433,    "marcato": 122881,
	"marimba": 4447,    "metalpad": 60905,  "metbell": 539,
	"metclick": 539,    "musicbox": 30947,  "mutegtr": 34577,
	"mutetrum": 19019,  "nyguitar": 39211,  "oboe": 9269,
	"ocarina": 3537,    "odguitar": 25845,  "orchhit": 28751,
	"percorg": 15435,   "piccolo": 8945,    "pickbass": 33213,
	"pistol": 36595,    "pizzcato": 40173,  "polysyn": 60759,
	"recorder": 5647,   "reedorg": 3471,    "revcym": 27391,
	"rockorg": 60887,   "santur": 43833,    "sawwave": 54485,
	"scratch1": 9091,   "scratch2": 4883,   "seashore": 62407,
	"shakazul": 62589,  "shaker": 6527,     "shamisen": 26667,
	"shannai": 20151,   "sitar": 36979,     "slap": 12031,
	"slapbas1": 56133,  "slapbas2": 41581,  "slowstr": 36717,
	"snare1": 17417,    "snare2": 8503,     "soundtrk": 40091,
	"sprnosax": 14713,  "sqrclick": 539,    "sqrwave": 30439,
	"startrak": 55085,  "steeldrm": 24229,  "stickrim": 6005,
	"sticks": 8757,     "surdo1": 19527,    "surdo2": 19527,
	"sweeper": 62745,   "synbass1": 12627,  "synbass2": 6191,
	"synbras1": 61735,  "synbras2": 60641,  "synpiano": 11543,
	"synstr1": 62763,   "synstr2": 33165,   "syntom": 61331,
	"taiko": 37671,     "tamborin": 18219,  "telephon": 9157,
	"tenorsax": 17367,  "timbaleh": 10839,  "timbalel": 19787,
	"timpani": 14473,   "tomhi1": 13467,    "tomhi2": 13455,
	"tomlo1": 13455,    "tomlo2": 19527,    "tommid1": 13455,
	"tommid2": 13455,   "toms": 13467,      "tremstr": 122881,
	"triangl1": 4781,   "triangl2": 31901,  "trombone": 26187,
	"trumpet": 13621,   "tuba": 11847,      "tubebell": 18637,
	"unicorn": 60505,   "vibes": 21597,     "vibslap": 19247,
	"viola": 56465,     "violin": 25061,    "voices": 30287,
	"voxlead": 30289,   "warmpad": 36491,   "whistle": 12053,
	"whistle1": 4315,   "whistle2": 2173,   "woodblk": 7685,
	"woodblk1": 5035,   "woodblk2": 7685,   "woodflut": 4191,
	"xylophon": 19085
}

def patches_for_mapping(patches, mapping):
	result = {}

	for pnum in mapping.values():
		patch = patches[pnum]
		result[patch] = True

	return sorted(result.keys())

def patch_set_size(patch_set):
	result = 0

	for patch in patch_set:
		result += GUS_PATCH_SIZES[patch]

	return result

def print_patch_set(title, patch_set):
	print "%s:" % title

	for patch in patch_set:
		print "\t%-8s    %i" % (patch, GUS_PATCH_SIZES[patch])

	print "\t" + ("-" * 30)
	print "\t%-8s    %i" % ("TOTAL", patch_set_size(patch_set))

patches = {}
mappings = [ {}, {}, {}, {} ]

f = open("ultramid.ini")

for line in f:
	line = line.strip()
	if line.startswith("#"):
		continue

	fields = re.split(r"\s*,\s*", line)

	instr = int(fields[0])
	patches[instr] = fields[5]

	for i in range(4):
		mappings[i][instr] = int(fields[i + 1])

f.close()

# Check mappings:

MAPPING_SIZES = [ 256, 512, 768, 1024 ]

for i in range(4):
	patch_set = patches_for_mapping(patches, mappings[i])

	if patch_set_size(patch_set) > MAPPING_SIZES[i] * 1024:
		print >> sys.stderr, \
		    "ERROR: Configuration for %iKB exceeds %iKB" % \
		    (MAPPING_SIZES[i], MAPPING_SIZES[i])
		print_patch_set(MAPPING_SIZES[i], patch_set)
		sys.exit(-1)

