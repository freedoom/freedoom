#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause
#
# Config file for GENMIDI file generation.
#
# This specifies the instrument files that should be used to generate
# the GENMIDI lump. Instrument files can be in SBI or A2I format.
# Instrument files must not use OPL3 features and it is an error to do so.
#
# A simple instrument specification looks like this:
#
#   Instrument("filename.sbi")
#
# For a double-voice instrument (two instrument files played at the same
# time), do this:
#
#   Instrument("file1.sbi", "file2.sbi")
#
# To tune the instruments, it's possible to apply an offset to the notes
# that are played. For example, to force all notes down by one octave:
#
#   Instrument("file1.sbi", off1=-12)
#
# This can be controlled individually for double-voice instruments, eg.
#
#   Instrument("file1.sbi", "file2.sbi", off1=-12, off2=+6)
#
# When an instrument is played, the note usually comes from the MIDI
# event. Some instruments (especially percussion) always play the same
# note. To specify a fixed note, do this:
#
#   Instrument("filename.sbi", note=On5.B)
#
# Value is a MIDI note number; see midi.py for constant definitions.

from instrument import Instrument, NullInstrument
from midi import *

# Note: all instruments must ALWAYS be defined, or use NullInstrument.

# General MIDI instruments:
INSTRUMENTS = [
	Instrument('instr001.sbi', 'instr001-2.sbi',  # Acoustic Grand Piano
	           off1=-12, off2=-12, tune=+2),
	Instrument('instr002.sbi', 'instr002-2.sbi',  # Bright Acoustic Piano
	           off1=-12, off2=-12, tune=+2),
	Instrument('instr003.sbi', 'instr003-2.sbi',  # Electric Grand Piano
	           tune=+2),
	Instrument('instr004.sbi', 'instr004-2.sbi',  # Honky-tonk Piano
	           off1=-12, off2=-12, tune=+10),
	Instrument('instr005.sbi', 'instr005-2.sbi',  # Electric Piano (Rhodes)
	           off1=-12, off2=-12, tune=+3),
	Instrument('instr006.sbi', 'instr006-2.sbi',  # Electric Piano (DX-7)
	           off1=-12, off2=-12, tune=+4),
	Instrument('instr007.sbi', 'instr007-2.sbi',  # Harpsichord
	           off1=-12, off2=-12),
	Instrument('instr008.sbi', 'instr008-2.sbi',  # Clavichord
	           off1=-12, off2=-12),
	Instrument('instr009.sbi', 'instr009-2.sbi',  # Celesta
	           off1=-12, off2=-12, tune=+1),
	Instrument('instr010.sbi', 'instr010-2.sbi',  # Glockenspiel
	           off1=-24, off2=-24),
	Instrument('instr011.sbi', 'instr011-2.sbi',  # Music Box
	           off1=-12, tune=+4),
	Instrument('instr012.sbi', 'instr012-2.sbi',  # Vibraphone
	           off1=-12, off2=-12),
	Instrument('instr013.sbi', 'instr013-2.sbi',  # Marimba
	           off2=-12),
	Instrument('instr014.sbi', off1=-12),         # Xylophone
	Instrument('instr015.sbi', 'instr015-2.sbi',  # Tubular Bells
	           off1=-24, off2=-24, tune=+2),
	Instrument('instr016.sbi', 'instr016-2.sbi',  # Dulcimer
	           off1=-12, off2=-12, tune=+2),
	Instrument('instr017.sbi', 'instr017-2.sbi',  # Drawbar Organ
	           off1=-12, tune=+10),
	Instrument('instr018.sbi', 'instr018-2.sbi',  # Percussive Organ
	           off1=-24, off2=-24),
	Instrument('instr019.sbi', 'instr019-2.sbi',  # Rock Organ
	           off1=-12, off2=-12, tune=+10),
	Instrument('instr020.sbi', 'instr020-2.sbi',  # Church Organ
	           off1=-12, off2=-12, tune=+2),
	Instrument('instr021.sbi', 'instr021-2.sbi',  # Reed Organ
	           off1=-12, off2=-12),
	Instrument('instr022.sbi', 'instr022-2.sbi',  # Accordion
	           off1=-12, off2=-12, tune=+9),
	Instrument('instr023.sbi', 'instr023-2.sbi',  # Harmonica (DMX FIXED)
	           off1=-12, off2=-12),
	Instrument('instr024.sbi', 'instr024-2.sbi',  # Tango Accordion
	           off1=-12, off2=-12, tune=+7),
	Instrument('instr025.sbi', 'instr025-2.sbi',  # Acoustic Guitar (nylon)
	           off1=-12, off2=-24),
	Instrument('instr026.sbi', 'instr026-2.sbi',  # Acoustic Guitar (steel)
	           off1=-12, off2=-12, tune=+1),
	Instrument('instr027.sbi', 'instr027-2.sbi',  # Electric Guitar (jazz)
	           off1=-12, off2=-12),
	Instrument('instr028.sbi', 'instr028-2.sbi',  # Electric Guitar (clean)
	           off1=-12, off2=-12, tune=+3),
	Instrument('instr029.sbi', 'instr029-2.sbi',  # Electric Guitar (muted)
	           off1=-12, off2=-12),
	Instrument('instr030.sbi', 'instr030-2.sbi',  # Overdriven Guitar
	           off1=-12, off2=+2, tune=-122),
	Instrument('instr031.sbi', 'instr031-2.sbi',  # Distortion Guitar
	           off1=-12, off2=+2, tune=-122),
	Instrument('instr032.sbi', 'instr032-2.sbi',  # Guitar Harmonics
	           off1=-12, off2=-12, tune=+15),
	Instrument('instr033.sbi', 'instr033-2.sbi',  # Acoustic Bass
	           off1=-12, off2=-12, tune=+2),
	Instrument('instr034.sbi', 'instr034-2.sbi'), # Electric Bass (finger)
	Instrument('instr035.sbi', 'instr035-2.sbi',  # Electric Bass (pick)
	           off1=-12),
	Instrument('instr036.sbi', 'instr036-2.sbi',  # Fretless Bass (DMX BUG FIX)
	           off1=-12, off2=-12, tune=+3),
	Instrument('instr037.sbi', 'instr037-2.sbi',  # Slap Bass 1
	           off1=-12, off2=-12),
	Instrument('instr038.sbi', 'instr038-2.sbi',  # Slap Bass 2
	           off1=-12, off2=-12),
	Instrument('instr039.sbi'),                   # Synth Bass 1
	Instrument('instr040.sbi', 'instr040-2.sbi',  # Synth Bass 2
	           off1=-12, off2=-12, tune=+10),
	Instrument('instr041.sbi', 'instr041-2.sbi',  # Violin
	           off1=-12, off2=-12),
	Instrument('instr042.sbi', off1=-12),         # Viola
	Instrument('instr043.sbi', 'instr043-2.sbi',  # Cello
	           off1=-12, off2=-12, tune=+1),
	Instrument('instr044.sbi', off1=-12),         # Contrabass
	Instrument('instr045.sbi', 'instr045-2.sbi',  # Tremolo Strings (DMX)
	           off2=-12, tune=+5),
	Instrument('instr046.sbi', 'instr046-2.sbi',  # Pizzicato String
	           off1=-12, off2=-12, tune=+10),
	Instrument('instr047.sbi', 'instr047-2.sbi',  # Orchestral Harp
	           off1=-12, off2=-12, tune=+2),
	Instrument('instr048.sbi', 'instr048-2.sbi',  # Timpani (DMX)
	           off1=-36, off2=-12, tune=+2),
	Instrument('instr049.sbi', 'instr049-2.sbi',  # String Ensemble 1 (DMX)
	           off2=-12, tune=+5),
	Instrument('instr050.sbi', 'instr050-2.sbi',  # String Ensemble 2 (DMX)
	           off2=-12, tune=+5),
	Instrument('instr051.sbi', 'instr051-2.sbi',  # SynthStrings 1
	           off1=-12, off2=-24, tune=+4),
	Instrument('instr052.sbi', 'instr052-2.sbi',  # SynthStrings 2
	           off1=-12, off2=-12, tune=+7),
	Instrument('instr053.sbi', 'instr053-2.sbi',  # Choir Aahs
	           off1=-12, off2=-24, tune=+9),
	Instrument('instr054.sbi', 'instr054-2.sbi',  # Voice Oohs
	           off1=-12, off2=-12, tune=+9),
	Instrument('instr055.sbi', 'instr055-2.sbi',  # Synth Voice
	           off1=-12, off2=-12, tune=+10),
	Instrument('instr056.sbi', 'instr056-2.sbi',  # Orchestra Hit
	           off1=-12, off2=-12, tune=+8),
	Instrument('instr057.sbi', off1=-12),         # Trumpet (DMX FIXED)
	Instrument('instr058.sbi', 'instr058-2.sbi',  # Trombone
	           off1=-12, off2=-12, tune=+2),
	Instrument('instr059.sbi', off1=-12),         # Tuba
	Instrument('instr060.sbi', off1=-24),         # Muted Trumpet
	Instrument('instr061.sbi', 'instr061-2.sbi',  # French Horn
	           off1=-12, off2=-12, tune=+2),
	Instrument('instr062.sbi', 'instr062-2.sbi',  # Brass Section
	           off1=-12, off2=-12, tune=+4),
	Instrument('instr063.sbi', 'instr063-2.sbi',  # Synth Brass 1
	           off1=-12, off2=-12, tune=+6),
	Instrument('instr064.sbi', 'instr064-2.sbi',  # Synth Brass 2
	           off1=-12, off2=-12, tune=+8),
	Instrument('instr065.sbi', off1=-12),         # Soprano Sax
	Instrument('instr066.sbi', off1=-12),         # Alto Sax
	Instrument('instr067.sbi'),                   # Tenor Sax
	Instrument('instr068.sbi'),                   # Baritone Sax
	Instrument('instr069.sbi', 'instr069-2.sbi',  # Oboe
	           off1=-12, off2=-12),
	Instrument('instr070.sbi', off1=-12),         # English Horn
	Instrument('instr071.sbi', off1=-12),         # Bassoon
	Instrument('instr072.sbi', off1=-12),         # Clarinet (DMX FIXED)
	Instrument('instr073.sbi', off1=-12),         # Piccolo
	Instrument('instr074.sbi', off1=-12),         # Flute
	Instrument('instr075.sbi', off1=-12),         # Recorder
	Instrument('instr076.sbi', 'instr076-2.sbi',  # Pan Flute (DMX)
	           off1=-12, off2=-12, tune=+2),
	Instrument('instr077.sbi', 'instr077-2.sbi',  # Blown Bottle
	           off1=-12, off2=-12, tune=+3),
	Instrument('instr078.sbi', 'instr078-2.sbi',  # Shakuhachi
	           off1=-12, off2=-12, tune=+2),
	Instrument('instr079.sbi', off1=-12),         # Whistle
	Instrument('instr080.sbi', off1=-12),         # Ocarina
	Instrument('instr081.sbi', 'instr081-2.sbi',  # Lead 1 (square)
	           off1=-12, off2=-12, tune=+8),
	Instrument('instr082.sbi', 'instr082-2.sbi',  # Lead 2 (sawtooth)
	           off1=-12, off2=-12, tune=+7),
	Instrument('instr083.sbi', 'instr083-2.sbi',  # Lead 3 (calliope)
	           off1=-12, off2=-12, tune=+7),
	Instrument('instr084.sbi', 'instr084-2.sbi',  # Lead 4 (chiffer)
	           off1=-12, off2=-12, tune=-2),
	Instrument('instr085.sbi', off1=-12),         # Lead 5 (charang)
	Instrument('instr086.sbi', 'instr086-2.sbi',  # Lead 6 (Voice)
	           off1=-12, off2=-12, tune=+10),
	Instrument('instr087.sbi', 'instr087-2.sbi',  # Lead 7 (5th sawtooth)
	           off2=-5, tune=-3),
	Instrument('instr088.sbi', 'instr088-2.sbi',  # Lead 8 (Lead+Bass)
	           tune=+2),
	Instrument('instr089.sbi', 'instr089-2.sbi',  # Pad 1 (new age)
	           off1=-12, off2=-12, tune=+5),
	Instrument('instr090.sbi', 'instr090-2.sbi',  # Pad 2 (warm)
	           off1=-12, off2=-12, tune=+7),
	Instrument('instr091.sbi', 'instr091-2.sbi',  # Pad 3 (polysynth)
	           off1=-12, off2=-12, tune=+5),
	Instrument('instr092.sbi', 'instr092-2.sbi',  # Pad 4 (choir)
	           off1=-12, off2=-12, tune=+10),
	Instrument('instr093.sbi', 'instr093-2.sbi',  # Pad 5 (bowed glass)
	           off1=-12, off2=-12, tune=+7),
	Instrument('instr094.sbi', 'instr094-2.sbi',  # Pad 6 (metal)
	           off1=-12, off2=-12, tune=+4),
	Instrument('instr095.sbi', 'instr095-2.sbi',  # Pad 7 (halo)
	           off1=-12, off2=-12, tune=+6),
	Instrument('instr096.sbi', 'instr096-2.sbi',  # Pad 8 (sweep)
	           off1=-12, off2=-12, tune=+7),
	Instrument('instr097.sbi', 'instr097-2.sbi',  # FX 1 (rain)
	           off1=-12, off2=-12, tune=+6),
	Instrument('instr098.sbi', 'instr098-2.sbi',  # FX 2 (soundtrack)
	           off1=-12, off2=-5, tune=+8),
	Instrument('instr099.sbi', 'instr099-2.sbi',  # FX 3 (crystal)
	           off1=-12, off2=-12, tune=+7),
	Instrument('instr100.sbi', 'instr100-2.sbi',  # FX 4 (atmosphere)
	           off1=-12, off2=-12, tune=-3),
	Instrument('instr101.sbi', 'instr101-2.sbi',  # FX 5 (brightness)
	           off1=-12, off2=-12, tune=+8),
	Instrument('instr102.sbi', 'instr102-2.sbi',  # FX 6 (goblin)
	           off1=-12, off2=-12, tune=-5),
	Instrument('instr103.sbi', 'instr103-2.sbi',  # FX 7 (echo drops)
	           off1=-12, off2=-12, tune=+9),
	Instrument('instr104.sbi', 'instr104-2.sbi',  # * FX 8 (star-theme)
	           off1=-12, off2=-12, tune=+5),
	Instrument('instr105.sbi', 'instr105-2.sbi',  # Sitar
	           off1=-12, off2=-12, tune=+2),
	Instrument('instr106.sbi', 'instr106-2.sbi',  # Banjo
	           off1=-12, off2=-12),
	Instrument("instr107.sbi", off1=-12),         # #107 - Shamisen
	Instrument('instr108.sbi', off1=-12),         # Koto
	Instrument('instr109.sbi', off1=-12),         # Kalimba
	Instrument('instr110.sbi', 'instr110-2.sbi',  # Bag Pipe
	           off1=-12, off2=-12, tune=+4),
	Instrument('instr111.sbi', off1=-12),         # Fiddle
	Instrument('instr112.sbi', off1=-12),         # Shanai
	Instrument('instr113.sbi', off1=-7),          # Tinkle Bell
	Instrument('instr114.sbi', off1=-12),         # Agogo
	Instrument('instr115.sbi', 'instr115-2.sbi',  # Steel Drums
	           off1=-12, off2=-12, tune=+2),
	Instrument('instr116.sbi', off1=-12),         # Woodblock
	Instrument('instr117.sbi', 'instr117-2.sbi',  # Taiko Drum (new)
	           off1=-24, off2=-12),
	Instrument('instr118.sbi', 'instr118-2.sbi',  # Melodic Tom
	           off1=-12),
	Instrument('instr119.sbi', 'instr119-2.sbi',  # Synth Drum
	           off1=-24, off2=-12),
	Instrument('instr120.sbi', 'instr120-2.sbi',  # Reverse Cymbal
	           off1=-12, tune=+7),
	Instrument('instr121.sbi', off1=-26),         # Guitar Fret Noise (DMX)
	Instrument('instr122.sbi', 'instr122-2.sbi',  # Breath Noise
	           off1=-12, off2=-12),
	Instrument('instr123.sbi', 'instr123-2.sbi',  # Seashore
	           note=O0.F, off1=-35, off2=-36),
	Instrument('instr124.sbi'),                   # Bird Tweet
	Instrument('instr125.sbi', 'instr125-2.sbi',  # Telephone Ring
	           off1=-36, off2=-32),
	Instrument('instr126.sbi', 'instr126-2.sbi',  # Helicopter
	           note=On4.F, off1=-48, off2=-26),
	Instrument('instr127.sbi', 'instr127-2.sbi',  # Applause
	           note=O0.F, off1=-48, off2=-47),
	Instrument('instr128.sbi', off1=-12),         # Gun Shot
]

# Percussion instruments:
PERCUSSION = [
	Instrument('perc35.sbi', note=On3.Cs),        # Acoustic Bass Drum
	Instrument("perc36.sbi", note=On4.A),         # #36 Bass Drum 1
	Instrument('perc37.sbi', 'perc37-2.sbi',      # Slide Stick
	           note=O0.Cs),
	Instrument('perc38.sbi', 'perc38-2.sbi',      # Acoustic Snare
	           note=On2.D, off1=-12),
	Instrument('perc39.sbi', 'perc39-2.sbi',      # Hand Clap
	           note=On2.Cs, off1=-12, off2=-14),
	Instrument('perc40.sbi', 'perc40-2.sbi',      # Electric Snare
	           note=On2.D, off1=-4, off2=-11),
	Instrument('perc41.sbi',                      # Low Floor Tom
	           note=On3.Gs, off1=-12),
	Instrument('perc42.sbi', 'perc42-2.sbi',      # Closed High-Hat
	           note=On1.C, off1=-17, off2=-12, tune=-122),
	Instrument('perc43.sbi',                      # High Floor Tom
	           note=On3.As, off1=-12),
	Instrument('perc44.sbi',                      # Pedal High Hat
	           note=On1.C, off1=-17),
	Instrument('perc45.sbi',                      # Low Tom
	           note=On2.Cs, off1=-12),
	Instrument('perc46.sbi', 'perc46-2.sbi',      # Open High Hat
	           note=On1.C, off1=-17, off2=-12, tune=-122),
	Instrument('perc47.sbi',                      # Low-Mid Tom
	           note=On2.E, off1=-12),
	Instrument('perc48.sbi',                      # Hi-Mid Tom
	           note=On2.G, off1=-12),
	Instrument('perc49.sbi', 'perc49-2.sbi',      # Crash Cymbal 1
	           note=O0.Cs, tune=+6),
	Instrument('perc50.sbi',                      # High Tom
	           note=On2.As, off1=-12),
	Instrument('perc51.sbi', 'perc51-2.sbi',      # Ride Cymbal 1
	           note=O0.C, tune=+4),
	Instrument('perc52.sbi', 'perc52-2.sbi',      # Chinses Cymbal
	           note=O1.G, off2=-1, tune=+5),
	Instrument('perc53.sbi',                      # Ride Bell
	           note=O0.D, off1=-12),
	Instrument('perc54.sbi', 'perc54-2.sbi',      # Tambourine
	           note=O1.Gs, tune=+8),
	Instrument('perc55.sbi', 'perc55-2.sbi',      # Splash Cymbal
	           note=O0.G, off1=-12, off2=-11, tune=+5),
	Instrument('perc56.sbi', note=On1.As),        # Cowbell
	Instrument('perc57.sbi', 'perc57-2.sbi',      # Crash Cymbal 2
	           note=O0.D, tune=+6),
	Instrument('perc58.sbi', note=On3.C),         # Vibraslap
	Instrument('perc59.sbi', note=O0.Cs),         # Ride Cymbal 2
	Instrument('perc60.sbi', 'perc60-2.sbi',      # High Bongo (New)
	           note=On2.F, off1=-6, off2=-12),
	Instrument('perc61.sbi', 'perc61-2.sbi',      # Low Bongo (New)
	           note=On3.B, off2=-12),
	Instrument('perc62.sbi', 'perc62-2.sbi',      # Mute high conga (New)
	           note=On3.F, off1=-12, off2=-2),
	Instrument('perc63.sbi', 'perc63-2.sbi',      # Open High Conga (New)
	           note=On2.F, off1=-4, off2=-12),
	Instrument('perc64.sbi', 'perc64-2.sbi',      # Low Conga (New)
	           note=On2.Cs, off1=-4, off2=-12),
	Instrument('perc65.sbi', note=On1.G),         # High Timbale
	Instrument('perc66.sbi', note=On1.C),         # Low Timbale
	Instrument('perc67.sbi', 'perc67-2.sbi',      # High Agogo
	           note=O1.Fs, off2=-6),
	Instrument('perc68.sbi', 'perc68-2.sbi',      # Low Agogo
	           note=O1.Cs, off2=-1),
	NullInstrument,                               # TODO - #69 Cabasa
	Instrument('perc70.sbi', note=On2.E),         # Maracas
	Instrument('perc71.sbi', note=On2.A),         # Short Whistle
	Instrument('perc72.sbi', note=On2.Fs),        # Long Whistle
	Instrument('perc73.sbi', 'perc73-2.sbi',      # Short Guiro
	           note=On1.C, off1=-12, off2=-12),
	Instrument('perc74.sbi', 'perc74-2.sbi',      # Long Guiro
	           note=On1.C, off1=-12, off2=-12),
	Instrument('perc75.sbi', note=O1.Cs),         # Claves
	Instrument("perc76.sbi", note=On5.E),         # #76 Hi Wood Block
	Instrument("perc77.sbi", note=On5.E),         # #77 Low Wood Block
	Instrument('perc78.sbi', note=On4.E),         # Mute Cuica
	Instrument('perc79.sbi', note=On4.E),         # Open Cuica
	Instrument('perc80.sbi', note=O2.Fs),         # Mute Triangle
	Instrument('perc81.sbi', note=O2.Fs),         # Open Triangle
]
