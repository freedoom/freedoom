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

# General MIDI instruments:

INSTRUMENTS = [
    Instrument("instr001.sbi"),  # #001 - Acoustic Grand Piano
    Instrument("instr002.sbi"),  # #002 - Bright Acoustic Piano
    Instrument("instr003.sbi"),  # #003 - Electric Grand Piano
    Instrument("instr004.sbi", "instr004-2.sbi"),  # #004 - Honky-tonk Piano
    Instrument("instr005.sbi", "instr005-2.sbi"),  # #005 - Electric Piano 1
    Instrument("instr006.sbi", off1=-12),  # #006 - Electric Piano 2
    Instrument("instr007.sbi"),  # #007 - Harpsichord
    Instrument("instr008.sbi", off1=-12),  # #008 - Clavi
    Instrument("instr009.sbi", off1=-12),  # #009 - Celesta
    Instrument("instr010.sbi", off1=-12),  # #010 - Glockenspiel
    Instrument("instr011.sbi", off1=-12),  # #011 - Music Box
    Instrument("instr012.sbi", off1=-12),  # #012 - Vibraphone
    Instrument("instr013.sbi", off1=-12),  # #013 - Marimba
    Instrument("instr014.sbi", off1=-12),  # #014 - Xylophone
    Instrument("instr015.sbi", off1=-12),  # #015 - Tubular Bells
    Instrument("instr016.sbi", off1=-12),  # #016 - Dulcimer
    Instrument("instr017.sbi", off1=-12),  # #017 - Drawbar Organ
    Instrument("instr018.sbi", off1=-12),  # #018 - Percussive Organ
    Instrument("instr019.sbi", off1=-12),  # #019 - Rock Organ
    Instrument("instr020.sbi", off1=-12),  # #020 - Church Organ
    Instrument("instr021.sbi", off1=-12),  # #021 - Reed Organ
    Instrument("instr022.sbi", off1=-12),  # #022 - Accordion
    Instrument("instr023.sbi", off1=-12),  # #023 - Harmonica
    Instrument("instr024.sbi", off1=-12),  # #024 - Tango Accordion
    Instrument("instr025.sbi", off1=-12),  # #025 - Acoustic Guitar (nylon)
    Instrument("instr026.sbi", off1=-12),  # #026 - Acoustic Guitar (steel)
    Instrument("instr027.sbi", off1=-12),  # #027 - Electric Guitar (jazz)
    Instrument("instr028.sbi", off1=-12),  # #028 - Electric Guitar (clean)
    Instrument("instr029.sbi", off1=-12),  # #029 - Electric Guitar (muted)
    Instrument("instr030.sbi", off1=-12),  # #030 - Overdriven Guitar
    Instrument("instr031.sbi", off1=-12),  # #031 - Distortion Guitar
    Instrument("instr032.sbi", off1=-12),  # #032 - Guitar harmonics
    Instrument("instr033.sbi", off1=-12),  # #033 - Acoustic Bass
    Instrument("instr034.sbi", off1=-12),  # #034 - Electric Bass (finger)
    Instrument("instr035.sbi", off1=-12),  # #035 - Electric Bass (pick)
    Instrument("instr036.sbi", off1=-12),  # #036 - Fretless Bass
    Instrument("instr037.sbi", off1=-12),  # #037 - Slap Bass 1
    Instrument("instr038.sbi", off1=-12),  # #038 - Slap Bass 2
    Instrument("instr039.sbi", off1=-12),  # #039 - Synth Bass 1
    Instrument("instr040.sbi", off1=-12),  # #040 - Synth Bass 2
    Instrument("instr041.sbi", off1=-12),  # #041 - Violin
    Instrument("instr042.sbi", off1=-12),  # #042 - Viola
    Instrument("instr043.sbi", off1=-12),  # #043 - Cello
    Instrument("instr044.sbi", off1=-12),  # #044 - Contrabass
    Instrument("instr045.sbi", off1=-12),  # #045 - Tremolo Strings
    Instrument("instr046.sbi", off1=-12),  # #046 - Pizzicato Strings
    Instrument("instr047.sbi", off1=-12),  # #047 - Orchestral Harp
    Instrument("instr048.sbi", off1=-12),  # #048 - Timpani
    Instrument("instr049.sbi", off1=-12),  # #049 - String Ensemble 1
    Instrument("instr050.sbi", off1=-12),  # #050 - String Ensemble 2
    Instrument("instr051.sbi", off1=-12),  # #051 - SynthStrings 1
    Instrument("instr052.sbi", off1=-12),  # #052 - SynthStrings 2
    Instrument("instr053.sbi", off1=-12),  # #053 - Choir Aahs
    Instrument("instr054.sbi", off1=-12),  # #054 - Voice Oohs
    Instrument("instr055.sbi", off1=-12),  # #055 - Synth Voice
    Instrument("instr056.sbi", off1=-12),  # #056 - Orchestra Hit
    Instrument("instr057.sbi", off1=-12),  # #057 - Trumpet
    Instrument("instr058.sbi", off1=-12),  # #058 - Trombone
    Instrument("instr059.sbi", off1=-12),  # #059 - Tuba
    Instrument("instr060.sbi", off1=-12),  # #060 - Muted Trumpet
    Instrument("instr061.sbi", off1=-12),  # #061 - French Horn
    Instrument("instr062.sbi", off1=-12),  # #062 - Brass Section
    Instrument("instr063.sbi", off1=-12),  # #063 - SynthBrass 1
    Instrument("instr064.sbi", off1=-12),  # #064 - SynthBrass 2
    Instrument("instr065.sbi", off1=-12),  # #065 - Soprano Sax
    Instrument("instr066.sbi", off1=-12),  # #066 - Alto Sax
    Instrument("instr067.sbi", off1=-12),  # #067 - Tenor Sax
    Instrument("instr068.sbi", off1=-12),  # #068 - Baritone Sax
    Instrument("instr069.sbi", off1=-12),  # #069 - Oboe
    Instrument("instr070.sbi", off1=-12),  # #070 - English Horn
    Instrument("instr071.sbi", off1=-12),  # #071 - Bassoon
    Instrument("instr072.sbi", off1=-12),  # #072 - Clarinet
    Instrument("instr073.sbi", off1=-12),  # #073 - Piccolo
    Instrument("instr074.sbi", off1=-12),  # #074 - Flute
    Instrument("instr075.sbi", off1=-12),  # #075 - Recorder
    Instrument("instr076.sbi", off1=-12),  # #076 - Pan Flute
    Instrument("instr077.sbi", off1=-12),  # #077 - Blown Bottle
    Instrument("instr078.sbi", off1=-12),  # #078 - Shakuhachi
    Instrument("instr079.sbi", off1=-12),  # #079 - Whistle
    Instrument("instr080.sbi", off1=-12),  # #080 - Ocarina
    Instrument("instr081.sbi", off1=-12),  # #081 - Lead 1 (square)
    Instrument("instr082.sbi"),  # #082 - Lead 2 (sawtooth)
    Instrument("instr083.sbi", off1=-12),  # #083 - Lead 3 (calliope)
    Instrument("instr084.sbi", off1=-12),  # #084 - Lead 4 (chiff)
    Instrument("instr085.sbi", off1=-12),  # #085 - Lead 5 (charang)
    Instrument("instr086.sbi", off1=-12),  # #086 - Lead 6 (voice)
    Instrument("instr087.sbi", off1=-12),  # #087 - Lead 7 (fifths)
    Instrument("instr088.sbi", off1=-12),  # #088 - Lead 8 (bass + lead)
    Instrument("instr089.sbi", off1=-12),  # #089 - Pad 1 (new age)
    Instrument("instr090.sbi", off1=-12),  # #090 - Pad 2 (warm)
    Instrument("instr091.sbi", off1=-12),  # #091 - Pad 3 (polysynth)
    Instrument("instr092.sbi", off1=-12),  # #092 - Pad 4 (choir)
    Instrument("instr093.sbi", off1=-12),  # #093 - Pad 5 (bowed)
    Instrument("instr094.sbi", off1=-12),  # #094 - Pad 6 (metallic)
    Instrument("instr095.sbi", off1=-12),  # #095 - Pad 7 (halo)
    Instrument("instr096.sbi", off1=-12),  # #096 - Pad 8 (sweep)
    Instrument("instr097.sbi", off1=-12),  # #097 - FX 1 (rain)
    Instrument("instr098.sbi", off1=-12),  # #098 - FX 2 (soundtrack)
    Instrument("instr099.sbi", off1=-12),  # #099 - FX 3 (crystal)
    Instrument("instr100.sbi", off1=-12),  # #100 - FX 4 (atmosphere)
    Instrument("instr101.sbi", off1=-12),  # #101 - FX 5 (brightness)
    Instrument("instr102.sbi", off1=-12),  # #102 - FX 6 (goblins)
    Instrument("instr103.sbi", off1=-12),  # #103 - FX 7 (echoes)
    Instrument("instr104.sbi", off1=-12),  # #104 - FX 8 (sci-fi)
    Instrument("instr105.sbi", off1=-12),  # #105 - Sitar
    Instrument("instr106.sbi", off1=-12),  # #106 - Banjo
    Instrument("instr107.sbi", off1=-12),  # #107 - Shamisen
    Instrument("instr108.sbi", off1=-12),  # #108 - Koto
    Instrument("instr109.sbi", off1=-12),  # #109 - Kalimba
    Instrument("instr110.sbi", off1=-12),  # #110 - Bag pipe
    Instrument("instr111.sbi", off1=-12),  # #111 - Fiddle
    Instrument("instr112.sbi", off1=-12),  # #112 - Shanai
    Instrument("instr113.sbi", off1=-12),  # #113 - Tinkle Bell
    Instrument("instr114.sbi", off1=-12),  # #114 - Agogo
    Instrument("instr115.sbi", off1=-12),  # #115 - Steel Drums
    Instrument("instr116.sbi", off1=-12),  # #116 - Woodblock
    Instrument("instr117.sbi", off1=-12),  # #117 - Taiko Drum
    Instrument("instr118.sbi", off1=-12),  # #118 - Melodic Tom
    Instrument("instr119.sbi", off1=-12),  # #119 - Synth Drum
    Instrument("instr120.sbi", off1=-12),  # #120 - Reverse Cymbal
    Instrument("instr121.sbi", off1=-12),  # #121 - Guitar Fret Noise
    Instrument("instr122.sbi", off1=-12),  # #122 - Breath Noise
    Instrument("instr123.sbi", off1=-12),  # #123 - Seashore
    Instrument("instr124.sbi", off1=-12),  # #124 - Bird Tweet
    Instrument("instr125.sbi", off1=-12),  # #125 - Telephone Ring
    Instrument("instr126.sbi", off1=-12),  # #126 - Helicopter
    Instrument("instr127.sbi", off1=-12),  # #127 - Applause
    Instrument("instr128.sbi", off1=-12),  # #128 - Gunshot
]

# Percussion instruments:
# Note: Many of these instruments have not been defined yet.
# As these are percussion instruments, a note number should ALWAYS be
# specified.

PERCUSSION = [
    Instrument("perc35.sbi", note=On4.A),  # #35 Acoustic Bass Drum
    Instrument("perc36.sbi", note=On4.A),  # #36 Bass Drum 1
    Instrument("perc37.sbi", note=On1.C),  # #37 Side Stick
    Instrument("perc38.sbi", note=On3.Gs),  # #38 Acoustic Snare
    Instrument("perc39.sbi", note=O3.C),  # #39 Hand Clap
    Instrument("perc40.sbi", note=On1.Cs),  # #40 Electric Snare
    Instrument("perc41.sbi", note=On3.D),  # #41 Low Floor Tom
    Instrument("perc42.sbi", note=O1.Gs),  # #42 Closed Hi Hat
    Instrument("perc43.sbi", note=On3.Gs),  # #43 High Floor Tom
    Instrument("perc44.sbi", note=O1.Gs),  # #44 Pedal Hi-Hat
    Instrument("perc45.sbi", note=On2.C),  # #45 Low Tom
    Instrument("perc46.sbi", note=O1.Gs),  # #46 Open Hi-Hat
    Instrument("perc47.sbi", note=On2.Fs),  # #47 Low-Mid Tom
    Instrument("perc48.sbi", note=On2.A),  # #48 Hi-Mid Tom
    Instrument("perc49.sbi", note=On1.C),  # #49 Crash Cymbal 1
    Instrument("perc50.sbi", note=On1.Cs),  # #50 High Tom
    Instrument("perc51.sbi", note=On1.B),  # #51 Ride Cymbal 1
    Instrument("perc52.sbi", note=On1.C),  # #52 Chinese Cymbal
    Instrument("perc53.sbi", note=O1.E),  # #53 Ride Bell
    Instrument("perc54.sbi", note=O0.E),  # #54 Tambourine
    NullInstrument,  # TODO - #55 Splash Cymbal
    NullInstrument,  # TODO - #56 Cowbell
    Instrument("perc57.sbi", note=On1.As),  # #57 Crash Cymbal 2
    NullInstrument,  # TODO - #58 Vibraslap
    Instrument("perc59.sbi", note=O0.E),  # #59 Ride Cymbal 2
    NullInstrument,  # TODO - #60 Hi Bongo
    NullInstrument,  # TODO - #61 Low Bongo
    NullInstrument,  # TODO - #62 Mute Hi Conga
    NullInstrument,  # TODO - #63 Open Hi Conga
    NullInstrument,  # TODO - #64 Low Conga
    NullInstrument,  # TODO - #65 High Timbale
    NullInstrument,  # TODO - #66 Low Timbale
    NullInstrument,  # TODO - #67 High Agogo
    NullInstrument,  # TODO - #68 Low Agogo
    NullInstrument,  # TODO - #69 Cabasa
    Instrument("perc70.sbi", note=On5.E),  # #70 Maracas
    Instrument("perc71.sbi", note=On5.E),  # #71 Short Whistle
    Instrument("perc72.sbi", note=On5.E),  # #72 Long Whistle
    Instrument("perc73.sbi", note=On5.E),  # #73 Short Guiro
    Instrument("perc74.sbi", note=On5.E),  # #74 Long Guiro
    Instrument("perc75.sbi", note=On5.E),  # #75 Claves
    Instrument("perc76.sbi", note=On5.E),  # #76 Hi Wood Block
    Instrument("perc77.sbi", note=On5.E),  # #77 Low Wood Block
    Instrument("perc78.sbi", note=On5.E),  # #78 Mute Cuica
    Instrument("perc79.sbi", note=On5.E),  # #79 Open Cuica
    Instrument("perc80.sbi", note=On5.E),  # #80 Mute Triangle
    Instrument("perc81.sbi", note=On5.E),  # #81 Open Triangle
]
