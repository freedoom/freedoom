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
# When an instrument is played, the note usually comes from the MIDI
# event. Some instruments (especially percussion) always play the same
# note. To specify a fixed note, do this:
#
#   Instrument("filename.sbi", note=16)
#
# (Where the value is the MIDI note number)

from instrument import Instrument, NullInstrument

# General MIDI instruments:

INSTRUMENTS = [
	Instrument("instr001.sbi"),             # #001 - Acoustic Grand Piano
	Instrument("instr002.sbi"),             # #002 - Bright Acoustic Piano
	Instrument("instr003.sbi"),             # #003 - Electric Grand Piano
	Instrument("instr004.sbi"),             # #004 - Honky-tonk Piano
	Instrument("instr005.sbi"),             # #005 - Electric Piano 1
	Instrument("instr006.sbi"),             # #006 - Electric Piano 2
	Instrument("instr007.sbi"),             # #007 - Harpsichord
	Instrument("instr008.sbi"),             # #008 - Clavi
	Instrument("instr009.sbi"),             # #009 - Celesta
	Instrument("instr010.sbi"),             # #010 - Glockenspiel
	Instrument("instr011.sbi"),             # #011 - Music Box
	Instrument("instr012.sbi"),             # #012 - Vibraphone
	Instrument("instr013.sbi"),             # #013 - Marimba
	Instrument("instr014.sbi"),             # #014 - Xylophone
	Instrument("instr015.sbi"),             # #015 - Tubular Bells
	Instrument("instr016.sbi"),             # #016 - Dulcimer
	Instrument("instr017.sbi"),             # #017 - Drawbar Organ
	Instrument("instr018.sbi"),             # #018 - Percussive Organ
	Instrument("instr019.sbi"),             # #019 - Rock Organ
	Instrument("instr020.sbi"),             # #020 - Church Organ
	Instrument("instr021.sbi"),             # #021 - Reed Organ
	Instrument("instr022.sbi"),             # #022 - Accordion
	Instrument("instr023.sbi"),             # #023 - Harmonica
	Instrument("instr024.sbi"),             # #024 - Tango Accordion
	Instrument("instr025.sbi"),             # #025 - Acoustic Guitar (nylon)
	Instrument("instr026.sbi"),             # #026 - Acoustic Guitar (steel)
	Instrument("instr027.sbi"),             # #027 - Electric Guitar (jazz)
	Instrument("instr028.sbi"),             # #028 - Electric Guitar (clean)
	Instrument("instr029.sbi"),             # #029 - Electric Guitar (muted)
	Instrument("instr030.sbi"),             # #030 - Overdriven Guitar
	Instrument("instr031.sbi"),             # #031 - Distortion Guitar
	Instrument("instr032.sbi"),             # #032 - Guitar harmonics
	Instrument("instr033.sbi"),             # #033 - Acoustic Bass
	Instrument("instr034.sbi"),             # #034 - Electric Bass (finger)
	Instrument("instr035.sbi"),             # #035 - Electric Bass (pick)
	Instrument("instr036.sbi"),             # #036 - Fretless Bass
	Instrument("instr037.sbi"),             # #037 - Slap Bass 1
	Instrument("instr038.sbi"),             # #038 - Slap Bass 2
	Instrument("instr039.sbi"),             # #039 - Synth Bass 1
	Instrument("instr040.sbi"),             # #040 - Synth Bass 2
	Instrument("instr041.sbi"),             # #041 - Violin
	Instrument("instr042.sbi"),             # #042 - Viola
	Instrument("instr043.sbi"),             # #043 - Cello
	Instrument("instr044.sbi"),             # #044 - Contrabass
	Instrument("instr045.sbi"),             # #045 - Tremolo Strings
	Instrument("instr046.sbi"),             # #046 - Pizzicato Strings
	Instrument("instr047.sbi"),             # #047 - Orchestral Harp
	Instrument("instr048.sbi"),             # #048 - Timpani
	Instrument("instr049.sbi"),             # #049 - String Ensemble 1
	Instrument("instr050.sbi"),             # #050 - String Ensemble 2
	Instrument("instr051.sbi"),             # #051 - SynthStrings 1
	Instrument("instr052.sbi"),             # #052 - SynthStrings 2
	Instrument("instr053.sbi"),             # #053 - Choir Aahs
	Instrument("instr054.sbi"),             # #054 - Voice Oohs
	Instrument("instr055.sbi"),             # #055 - Synth Voice
	Instrument("instr056.sbi"),             # #056 - Orchestra Hit
	Instrument("instr057.sbi"),             # #057 - Trumpet
	Instrument("instr058.sbi"),             # #058 - Trombone
	Instrument("instr059.sbi"),             # #059 - Tuba
	Instrument("instr060.sbi"),             # #060 - Muted Trumpet
	Instrument("instr061.sbi"),             # #061 - French Horn
	Instrument("instr062.sbi"),             # #062 - Brass Section
	Instrument("instr063.sbi"),             # #063 - SynthBrass 1
	Instrument("instr064.sbi"),             # #064 - SynthBrass 2
	Instrument("instr065.sbi"),             # #065 - Soprano Sax
	Instrument("instr066.sbi"),             # #066 - Alto Sax
	Instrument("instr067.sbi"),             # #067 - Tenor Sax
	Instrument("instr068.sbi"),             # #068 - Baritone Sax
	Instrument("instr069.sbi"),             # #069 - Oboe
	Instrument("instr070.sbi"),             # #070 - English Horn
	Instrument("instr071.sbi"),             # #071 - Bassoon
	Instrument("instr072.sbi"),             # #072 - Clarinet
	Instrument("instr073.sbi"),             # #073 - Piccolo
	Instrument("instr074.sbi"),             # #074 - Flute
	Instrument("instr075.sbi"),             # #075 - Recorder
	Instrument("instr076.sbi"),             # #076 - Pan Flute
	Instrument("instr077.sbi"),             # #077 - Blown Bottle
	Instrument("instr078.sbi"),             # #078 - Shakuhachi
	Instrument("instr079.sbi"),             # #079 - Whistle
	Instrument("instr080.sbi"),             # #080 - Ocarina
	Instrument("instr081.sbi"),             # #081 - Lead 1 (square)
	Instrument("instr082.sbi"),             # #082 - Lead 2 (sawtooth)
	Instrument("instr083.sbi"),             # #083 - Lead 3 (calliope)
	Instrument("instr084.sbi"),             # #084 - Lead 4 (chiff)
	Instrument("instr085.sbi"),             # #085 - Lead 5 (charang)
	Instrument("instr086.sbi"),             # #086 - Lead 6 (voice)
	Instrument("instr087.sbi"),             # #087 - Lead 7 (fifths)
	Instrument("instr088.sbi"),             # #088 - Lead 8 (bass + lead)
	Instrument("instr089.sbi"),             # #089 - Pad 1 (new age)
	Instrument("instr090.sbi"),             # #090 - Pad 2 (warm)
	Instrument("instr091.sbi"),             # #091 - Pad 3 (polysynth)
	Instrument("instr092.sbi"),             # #092 - Pad 4 (choir)
	Instrument("instr093.sbi"),             # #093 - Pad 5 (bowed)
	Instrument("instr094.sbi"),             # #094 - Pad 6 (metallic)
	Instrument("instr095.sbi"),             # #095 - Pad 7 (halo)
	Instrument("instr096.sbi"),             # #096 - Pad 8 (sweep)
	Instrument("instr097.sbi"),             # #097 - FX 1 (rain)
	Instrument("instr098.sbi"),             # #098 - FX 2 (soundtrack)
	Instrument("instr099.sbi"),             # #099 - FX 3 (crystal)
	Instrument("instr100.sbi"),             # #100 - FX 4 (atmosphere)
	Instrument("instr101.sbi"),             # #101 - FX 5 (brightness)
	Instrument("instr102.sbi"),             # #102 - FX 6 (goblins)
	Instrument("instr103.sbi"),             # #103 - FX 7 (echoes)
	Instrument("instr104.sbi"),             # #104 - FX 8 (sci-fi)
	Instrument("instr105.sbi"),             # #105 - Sitar
	Instrument("instr106.sbi"),             # #106 - Banjo
	Instrument("instr107.sbi"),             # #107 - Shamisen
	Instrument("instr108.sbi"),             # #108 - Koto
	Instrument("instr109.sbi"),             # #109 - Kalimba
	Instrument("instr110.sbi"),             # #110 - Bag pipe
	Instrument("instr111.sbi"),             # #111 - Fiddle
	Instrument("instr112.sbi"),             # #112 - Shanai
	Instrument("instr113.sbi"),             # #113 - Tinkle Bell
	Instrument("instr114.sbi"),             # #114 - Agogo
	Instrument("instr115.sbi"),             # #115 - Steel Drums
	Instrument("instr116.sbi"),             # #116 - Woodblock
	Instrument("instr117.sbi"),             # #117 - Taiko Drum
	Instrument("instr118.sbi"),             # #118 - Melodic Tom
	Instrument("instr119.sbi"),             # #119 - Synth Drum
	Instrument("instr120.sbi"),             # #120 - Reverse Cymbal
	Instrument("instr121.sbi"),             # #121 - Guitar Fret Noise
	Instrument("instr122.sbi"),             # #122 - Breath Noise
	Instrument("instr123.sbi"),             # #123 - Seashore
	Instrument("instr124.sbi"),             # #124 - Bird Tweet
	Instrument("instr125.sbi"),             # #125 - Telephone Ring
	Instrument("instr126.sbi"),             # #126 - Helicopter
	Instrument("instr127.sbi"),             # #127 - Applause
	Instrument("instr128.sbi"),             # #128 - Gunshot
]

# Percussion instruments:
# Note: Many of these instruments have not been defined yet.
# As these are percussion instruments, a note number should ALWAYS be
# specified.

PERCUSSION = [
	NullInstrument,                         # TODO - #35 Acoustic Bass Drum
	NullInstrument,                         # TODO - #36 Bass Drum 1
	NullInstrument,                         # TODO - #37 Side Stick
	NullInstrument,                         # TODO - #38 Acoustic Snare
	NullInstrument,                         # TODO - #39 Hand Clap
	NullInstrument,                         # TODO - #40 Electric Snare
	NullInstrument,                         # TODO - #41 Low Floor Tom
	NullInstrument,                         # TODO - #42 Closed Hi Hat
	NullInstrument,                         # TODO - #43 High Floor Tom
	NullInstrument,                         # TODO - #44 Pedal Hi-Hat
	NullInstrument,                         # TODO - #45 Low Tom
	NullInstrument,                         # TODO - #46 Open Hi-Hat
	NullInstrument,                         # TODO - #47 Low-Mid Tom
	NullInstrument,                         # TODO - #48 Hi-Mid Tom
	NullInstrument,                         # TODO - #49 Crash Cymbal 1
	NullInstrument,                         # TODO - #50 High Tom
	NullInstrument,                         # TODO - #51 Ride Cymbal 1
	NullInstrument,                         # TODO - #52 Chinese Cymbal
	NullInstrument,                         # TODO - #53 Ride Bell
	NullInstrument,                         # TODO - #54 Tambourine
	NullInstrument,                         # TODO - #55 Splash Cymbal
	NullInstrument,                         # TODO - #56 Cowbell
	NullInstrument,                         # TODO - #57 Crash Cymbal 2
	NullInstrument,                         # TODO - #58 Vibraslap
	NullInstrument,                         # TODO - #59 Ride Cymbal 2
	NullInstrument,                         # TODO - #60 Hi Bongo
	NullInstrument,                         # TODO - #61 Low Bongo
	NullInstrument,                         # TODO - #62 Mute Hi Conga
	NullInstrument,                         # TODO - #63 Open Hi Conga
	NullInstrument,                         # TODO - #64 Low Conga
	NullInstrument,                         # TODO - #65 High Timbale
	NullInstrument,                         # TODO - #66 Low Timbale
	NullInstrument,                         # TODO - #67 High Agogo
	NullInstrument,                         # TODO - #68 Low Agogo
	NullInstrument,                         # TODO - #69 Cabasa
	Instrument("perc70.sbi", note=16),      # #70 Maracas
	Instrument("perc71.sbi", note=16),      # #71 Short Whistle
	Instrument("perc72.sbi", note=16),      # #72 Long Whistle
	Instrument("perc73.sbi", note=16),      # #73 Short Guiro
	Instrument("perc74.sbi", note=16),      # #74 Long Guiro
	Instrument("perc75.sbi", note=16),      # #75 Claves
	Instrument("perc76.sbi", note=16),      # #76 Hi Wood Block
	Instrument("perc77.sbi", note=16),      # #77 Low Wood Block
	Instrument("perc78.sbi", note=16),      # #78 Mute Cuica
	Instrument("perc79.sbi", note=16),      # #79 Open Cuica
	Instrument("perc80.sbi", note=16),      # #80 Mute Triangle
	Instrument("perc81.sbi", note=16),      # #81 Open Triangle
]

