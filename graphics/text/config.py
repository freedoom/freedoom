#
# Copyright (c) 2013
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
# Configuration file for textgen. This file defines the graphic lumps
# that are generated, and the text to show in each one.
#

import re

# Adjustments for character position based on character pairs. Some
# pairs of characters can fit more snugly together, which looks more
# visually appealing. This is highly dependent on the font graphics,
# and if the font is changed this probably needs to be redone.

FONT_KERNING_RULES = {
	# Right character fits under left character:
	r'p[aj\.]': -3,
	r'P[a\.]': -4,
	r'[PVW][AJj\.]': -4,
	r't[ajJ\.]': -4,
	r'f[aj\.]': -2,

	# Some capital letters have overhangs that the 'lower case'
	# characters can fit under:
	r'C[Ja-z\.]': -2,
	r'F[Ja-z\.]': -3,
	r'T[Ja-z\.]': -5,
	r'W[Ja-z\.]': -2,
	r'S[Ja-z\.]': -1,
	r'V[a-z\.]': -3,

	# Left character fits under right character:
	r'[alAL][ty479]': -3,
	r'a[vwVW]': -2,
	r'A[VW]': -3,
	r'A[vw]': -2,
	r'r[ty479]': -2,
	r'[vwVW][Aa]': -2,
	r'[Yypv][jJ]': -2,

	# Extra space needed:
	r'[OUu][Pp]': +1,
}

white_graphics = {
	'wibp1': 'P1',
	'wibp2': 'P2',
	'wibp3': 'P3',
	'wibp4': 'P4',
	'wicolon': ':',

	# Note: level names are also included in this dictionary, with
	# the data added programatically from the DEHACKED lump, see
	# code below.
}

blue_graphics = {
	'm_disopt': 'DISPLAY OPTIONS',
	'm_episod': 'Choose Episode:',
	'm_optttl': 'OPTIONS',
	'm_skill': 'Choose Skill Level:',
}

red_graphics = {
	'm_ngame': 'New Game',
	'm_option': 'Options',
	'm_loadg': 'Load Game',
	'm_saveg': 'Save Game',
	'm_rdthis': 'Read This!',
	'm_quitg': 'Quit Game',

	'm_newg': 'NEW GAME',
	'm_epi1': 'First Episode',
	'm_epi2': 'Second Episode',
	'm_epi3': 'Third Episode',
	'm_epi4': 'Double Impact',

	'm_jkill': 'Please don\'t kill me!',
	'm_rough': 'Will this hurt?',
	'm_hurt': 'Bring on the pain.',
	'm_ultra': 'Extreme Carnage',
	'm_nmare': 'INSANITY!',

	'm_lgttl': 'LOAD GAME',
	'm_sgttl': 'SAVE GAME',

	'm_endgam': 'End Game',
	'm_messg': 'Messages:',
	'm_msgoff': 'off',
	'm_msgon': 'on',
	'm_msens': 'Mouse Sensitivity',
	'm_detail': 'Graphic Detail:',
	'm_gdhigh': 'high',
	'm_gdlow': 'low',
	'm_scrnsz': 'Screen Size',

	'm_svol': 'Sound Volume',
	'm_sfxvol': 'Sfx Volume',
	'm_musvol': 'Music Volume',

	'm_disp': 'Display',

	'wif': 'finished',
	'wiostk': 'kills',
	'wiosti': 'items',
	'wiscrt2': 'secret',
	'wiosts': 'scrt',
	'wifrgs': 'frgs',

	'witime': 'Time:',
	'wisucks': 'sucks',
	'wimstt': 'Total:',
	'wipar': 'Par:',
	'wip1': 'P1', 'wip2': 'P2', 'wip3': 'P3', 'wip4': 'P4',
	'wiostf': 'f.',
	'wimstar': 'you',
	'winum0': '0', 'winum1': '1', 'winum2': '2', 'winum3': '3',
	'winum4': '4', 'winum5': '5', 'winum6': '6', 'winum7': '7',
	'winum8': '8', 'winum9': '9',
	'wipcnt': '%',
	'wiminus': '-',
	'wienter': 'ENTERING',

	'm_pause': 'pause',

	# Extra graphics used in PrBoom's menus. Generate these as well
	# so that when we play in PrBoom the menus look consistent.
	'prboom': 'PrBoom',
	'm_generl': 'General',
	'm_setup': 'Setup',
	'm_keybnd': 'Key Bindings',
	'm_weap': 'Weapons',
	'm_stat': 'Status Bar/HUD',
	'm_auto': 'Automap',
	'm_enem': 'Enemies',
	'm_mess': 'Messages',
	'm_chat': 'Chat Strings',

	'm_horsen': 'horizontal',
	'm_versen': 'vertical',
	'm_loksen': 'mouse look',
	'm_accel': 'acceleration',

	# Extra graphics from SMMU/Eternity Engine:
	'm_about': 'about',
	'm_chatm': 'Chat Strings',
	'm_compat': 'Compatibility',
	'm_demos': 'demos',
	'm_dmflag': 'deathmatch flags',
	'm_etcopt': 'eternity options',
	'm_feat': 'Features',
	'm_gset': 'game settings',
	'm_hud': 'heads up display',
	'm_joyset': 'joysticks',
	'm_ldsv': 'Load/Save',
	'm_menus': 'Menu Options',
	'm_mouse': 'mouse options',
	'm_multi': 'multiplayer',
	'm_player': 'player setup',
	'm_serial': 'serial connection',
	'm_sound': 'sound options',
	'm_status': 'status bar',
	'm_tcpip': 'tcp/ip connection',
	'm_video': 'video options',
	'm_wad': 'load wad',
	'm_wadopt': 'wad options',
}

def read_bex_lump(filename):
	"""Read the BEX (Dehacked) lump from the given filename.

	Returns:
	    Dictionary mapping from name to value.
	"""
	result = {}
	with open(filename) as f:
		for line in f:
			# Ignore comments:
			line = line.strip()
			if len(line) == 0 or line[0] in '#;':
				continue
			# Just split on '=' and interpret that as an
			# assignment. This is primitive and doesn't read
			# like a full BEX parser should, but it's good
			# enough for our purposes here.
			assign = line.split('=', 2)
			if len(assign) != 2:
				continue
			result[assign[0].strip()] = assign[1].strip()
	return result

def update_level_name(lumpname, bexdata, bexname):
	"""Set the level name for the given graphic from BEX file.

	Args:
	  lumpname: Name of output graphic file.
	  bexdata: Dictionary of data read from BEX file.
	  bexname: Name of entry in BEX file to use.
	"""
	if bexname not in bexdata:
		raise Exception('Level name %s not defined in '
				'DEHACKED lump!' % bexname)
	# Strip "MAP01: " or "E1M2: " etc. from start, if present:
	levelname = re.sub('^\w*\d:\s*', '', bexdata[bexname])
	white_graphics[lumpname] = levelname

freedoom_bex = read_bex_lump('../../lumps/dehacked.lmp')
freedm_bex = read_bex_lump('../../lumps/fdm_deh.lmp')

for e in range(4):
	for m in range(9):
		# HUSTR_E1M1 from BEX => wilv00
		update_level_name('wilv%i%i' % (e, m), freedoom_bex,
		                  'HUSTR_E%iM%i' % (e + 1, m + 1))

for m in range(32):
	# HUSTR_1 => cwilv00
	update_level_name('cwilv%02i' % m, freedoom_bex, 'HUSTR_%i' % (m + 1))
	# HUSTR_1 => dmwilv00 (from freedm.bex)
	update_level_name('dmwilv%02i' % m, freedm_bex, 'HUSTR_%i' % (m + 1))

