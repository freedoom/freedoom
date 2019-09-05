# SPDX-License-Identifier: BSD-3-Clause
#
# Config file for GUS config generator.
#

# Names of GUS instrument files to use for playing MIDI.
# These are the names of the .pat files in the \ultrasnd\midi directory
# that are loaded into the card.

GUS_INSTR_PATCHES = {
    0: "acpiano",  # #001 - Acoustic Grand Piano
    1: "britepno",  # #002 - Bright Acoustic Piano
    2: "synpiano",  # #003 - Electric Grand Piano
    3: "honky",  # #004 - Honky-tonk Piano
    4: "epiano1",  # #005 - Electric Piano 1
    5: "epiano2",  # #006 - Electric Piano 2
    6: "hrpschrd",  # #007 - Harpsichord
    7: "clavinet",  # #008 - Clavi
    8: "celeste",  # #009 - Celesta
    9: "glocken",  # #010 - Glockenspiel
    10: "musicbox",  # #011 - Music Box
    11: "vibes",  # #012 - Vibraphone
    12: "marimba",  # #013 - Marimba
    13: "xylophon",  # #014 - Xylophone
    14: "tubebell",  # #015 - Tubular Bells
    15: "santur",  # #016 - Dulcimer
    16: "homeorg",  # #017 - Drawbar Organ
    17: "percorg",  # #018 - Percussive Organ
    18: "rockorg",  # #019 - Rock Organ
    19: "church",  # #020 - Church Organ
    20: "reedorg",  # #021 - Reed Organ
    21: "accordn",  # #022 - Accordion
    22: "harmonca",  # #023 - Harmonica
    23: "concrtna",  # #024 - Tango Accordion
    24: "nyguitar",  # #025 - Acoustic Guitar (nylon)
    25: "acguitar",  # #026 - Acoustic Guitar (steel)
    26: "jazzgtr",  # #027 - Electric Guitar (jazz)
    27: "cleangtr",  # #028 - Electric Guitar (clean)
    28: "mutegtr",  # #029 - Electric Guitar (muted)
    29: "odguitar",  # #030 - Overdriven Guitar
    30: "distgtr",  # #031 - Distortion Guitar
    31: "gtrharm",  # #032 - Guitar harmonics
    32: "acbass",  # #033 - Acoustic Bass
    33: "fngrbass",  # #034 - Electric Bass (finger)
    34: "pickbass",  # #035 - Electric Bass (pick)
    35: "fretless",  # #036 - Fretless Bass
    36: "slapbas1",  # #037 - Slap Bass 1
    37: "slapbas2",  # #038 - Slap Bass 2
    38: "synbass1",  # #039 - Synth Bass 1
    39: "synbass2",  # #040 - Synth Bass 2
    40: "violin",  # #041 - Violin
    41: "viola",  # #042 - Viola
    42: "cello",  # #043 - Cello
    43: "contraba",  # #044 - Contrabass
    44: "tremstr",  # #045 - Tremolo Strings
    45: "pizzcato",  # #046 - Pizzicato Strings
    46: "harp",  # #047 - Orchestral Harp
    47: "timpani",  # #048 - Timpani
    48: "marcato",  # #049 - String Ensemble 1
    49: "slowstr",  # #050 - String Ensemble 2
    50: "synstr1",  # #051 - SynthStrings 1
    51: "synstr2",  # #052 - SynthStrings 2
    52: "choir",  # #053 - Choir Aahs
    53: "doo",  # #054 - Voice Oohs
    54: "voices",  # #055 - Synth Voice
    55: "orchhit",  # #056 - Orchestra Hit
    56: "trumpet",  # #057 - Trumpet
    57: "trombone",  # #058 - Trombone
    58: "tuba",  # #059 - Tuba
    59: "mutetrum",  # #060 - Muted Trumpet
    60: "frenchrn",  # #061 - French Horn
    61: "hitbrass",  # #062 - Brass Section
    62: "synbras1",  # #063 - SynthBrass 1
    63: "synbras2",  # #064 - SynthBrass 2
    64: "sprnosax",  # #065 - Soprano Sax
    65: "altosax",  # #066 - Alto Sax
    66: "tenorsax",  # #067 - Tenor Sax
    67: "barisax",  # #068 - Baritone Sax
    68: "oboe",  # #069 - Oboe
    69: "englhorn",  # #070 - English Horn
    70: "bassoon",  # #071 - Bassoon
    71: "clarinet",  # #072 - Clarinet
    72: "piccolo",  # #073 - Piccolo
    73: "flute",  # #074 - Flute
    74: "recorder",  # #075 - Recorder
    75: "woodflut",  # #076 - Pan Flute
    76: "bottle",  # #077 - Blown Bottle
    77: "shakazul",  # #078 - Shakuhachi
    78: "whistle",  # #079 - Whistle
    79: "ocarina",  # #080 - Ocarina
    80: "sqrwave",  # #081 - Lead 1 (square)
    81: "sawwave",  # #082 - Lead 2 (sawtooth)
    82: "calliope",  # #083 - Lead 3 (calliope)
    83: "chiflead",  # #084 - Lead 4 (chiff)
    84: "charang",  # #085 - Lead 5 (charang)
    85: "voxlead",  # #086 - Lead 6 (voice)
    86: "lead5th",  # #087 - Lead 7 (fifths)
    87: "basslead",  # #088 - Lead 8 (bass + lead)
    88: "fantasia",  # #089 - Pad 1 (new age)
    89: "warmpad",  # #090 - Pad 2 (warm)
    90: "polysyn",  # #091 - Pad 3 (polysynth)
    91: "ghostie",  # #092 - Pad 4 (choir)
    92: "bowglass",  # #093 - Pad 5 (bowed)
    93: "metalpad",  # #094 - Pad 6 (metallic)
    94: "halopad",  # #095 - Pad 7 (halo)
    95: "sweeper",  # #096 - Pad 8 (sweep)
    96: "aurora",  # #097 - FX 1 (rain)
    97: "soundtrk",  # #098 - FX 2 (soundtrack)
    98: "crystal",  # #099 - FX 3 (crystal)
    99: "atmosphr",  # #100 - FX 4 (atmosphere)
    100: "freshair",  # #101 - FX 5 (brightness)
    101: "unicorn",  # #102 - FX 6 (goblins)
    102: "echovox",  # #103 - FX 7 (echoes)
    103: "startrak",  # #104 - FX 8 (sci-fi)
    104: "sitar",  # #105 - Sitar
    105: "banjo",  # #106 - Banjo
    106: "shamisen",  # #107 - Shamisen
    107: "koto",  # #108 - Koto
    108: "kalimba",  # #109 - Kalimba
    109: "bagpipes",  # #110 - Bag pipe
    110: "fiddle",  # #111 - Fiddle
    111: "shannai",  # #112 - Shanai
    112: "carillon",  # #113 - Tinkle Bell
    113: "agogo",  # #114 - Agogo
    114: "steeldrm",  # #115 - Steel Drums
    115: "woodblk",  # #116 - Woodblock
    116: "taiko",  # #117 - Taiko Drum
    117: "toms",  # #118 - Melodic Tom
    118: "syntom",  # #119 - Synth Drum
    119: "revcym",  # #120 - Reverse Cymbal
    120: "fx-fret",  # #121 - Guitar Fret Noise
    121: "fx-blow",  # #122 - Breath Noise
    122: "seashore",  # #123 - Seashore
    123: "jungle",  # #124 - Bird Tweet
    124: "telephon",  # #125 - Telephone Ring
    125: "helicptr",  # #126 - Helicopter
    126: "applause",  # #127 - Applause
    127: "pistol",  # #128 - Gunshot
    128: "blank",
    163: "kick1",  # #35 Acoustic Bass Drum
    164: "kick2",  # #36 Bass Drum 1
    165: "stickrim",  # #37 Side Stick
    166: "snare1",  # #38 Acoustic Snare
    167: "claps",  # #39 Hand Clap
    168: "snare2",  # #40 Electric Snare
    169: "tomlo2",  # #41 Low Floor Tom
    170: "hihatcl",  # #42 Closed Hi Hat
    171: "tomlo1",  # #43 High Floor Tom
    172: "hihatpd",  # #44 Pedal Hi-Hat
    173: "tommid2",  # #45 Low Tom
    174: "hihatop",  # #46 Open Hi-Hat
    175: "tommid1",  # #47 Low-Mid Tom
    176: "tomhi2",  # #48 Hi-Mid Tom
    177: "cymcrsh1",  # #49 Crash Cymbal 1
    178: "tomhi1",  # #50 High Tom
    179: "cymride1",  # #51 Ride Cymbal 1
    180: "cymchina",  # #52 Chinese Cymbal
    181: "cymbell",  # #53 Ride Bell
    182: "tamborin",  # #54 Tambourine
    183: "cymsplsh",  # #55 Splash Cymbal
    184: "cowbell",  # #56 Cowbell
    185: "cymcrsh2",  # #57 Crash Cymbal 2
    186: "vibslap",  # #58 Vibraslap
    187: "cymride2",  # #59 Ride Cymbal 2
    188: "bongohi",  # #60 Hi Bongo
    189: "bongolo",  # #61 Low Bongo
    190: "congahi1",  # #62 Mute Hi Conga
    191: "congahi2",  # #63 Open Hi Conga
    192: "congalo",  # #64 Low Conga
    193: "timbaleh",  # #65 High Timbale
    194: "timbalel",  # #66 Low Timbale
    195: "agogohi",  # #67 High Agogo
    196: "agogolo",  # #68 Low Agogo
    197: "cabasa",  # #69 Cabasa
    198: "maracas",  # #70 Maracas
    199: "whistle1",  # #71 Short Whistle
    200: "whistle2",  # #72 Long Whistle
    201: "guiro1",  # #73 Short Guiro
    202: "guiro2",  # #74 Long Guiro
    203: "clave",  # #75 Claves
    204: "woodblk1",  # #76 Hi Wood Block
    205: "woodblk2",  # #77 Low Wood Block
    206: "cuica1",  # #78 Mute Cuica
    207: "cuica2",  # #79 Open Cuica
    208: "triangl1",  # #80 Mute Triangle
    209: "triangl2",  # #81 Open Triangle
}

# These are the data sizes of the patch files distributed with the
# GUS drivers. These are used to calculate the size in RAM of the
# generated patch sets to check that they are within the limits.
# and check it is within the limit.

PATCH_FILE_SIZES = {
    "acbass": 5248,
    "accordn": 9616,
    "acguitar": 26080,
    "acpiano": 32256,
    "agogo": 13696,
    "agogohi": 3488,
    "agogolo": 3488,
    "altosax": 5616,
    "applause": 30064,
    "atmosphr": 31360,
    "aurora": 31088,
    "bagpipes": 7760,
    "banjo": 32016,
    "barisax": 10544,
    "basslead": 26496,
    "bassoon": 8000,
    "belltree": 31888,
    "blank": 1520,
    "bongohi": 3456,
    "bongolo": 4448,
    "bottle": 12368,
    "bowglass": 24688,
    "britepno": 36000,
    "cabasa": 8448,
    "calliope": 22992,
    "carillon": 5888,
    "castinet": 6016,
    "celeste": 9936,
    "cello": 9120,
    "charang": 45056,
    "chiflead": 31536,
    "choir": 22480,
    "church": 2144,
    "claps": 5696,
    "clarinet": 9184,
    "clave": 2352,
    "clavinet": 1440,
    "cleangtr": 22768,
    "concrtna": 8784,
    "congahi1": 4224,
    "congahi2": 4704,
    "congalo": 4704,
    "contraba": 4704,
    "cowbell": 3168,
    "crystal": 30224,
    "cuica1": 9344,
    "cuica2": 12848,
    "cymbell": 17248,
    "cymchina": 24112,
    "cymcrsh1": 31520,
    "cymcrsh2": 31040,
    "cymride1": 17664,
    "cymride2": 17664,
    "cymsplsh": 31520,
    "distgtr": 18848,
    "doo": 8464,
    "echovox": 14976,
    "englhorn": 12096,
    "epiano1": 7344,
    "epiano2": 21936,
    "fantasia": 23456,
    "fiddle": 5904,
    "flute": 6032,
    "fngrbass": 9744,
    "frenchrn": 14128,
    "freshair": 28992,
    "fretless": 2640,
    "fx-blow": 28688,
    "fx-fret": 13648,
    "ghostie": 31488,
    "glocken": 5184,
    "gtrharm": 4928,
    "guiro1": 4128,
    "guiro2": 9248,
    "halopad": 29984,
    "harmonca": 7408,
    "harp": 11728,
    "helicptr": 25008,
    "highq": 1808,
    "hihatcl": 4560,
    "hihatop": 20048,
    "hihatpd": 1808,
    "hitbrass": 31520,
    "homeorg": 992,
    "honky": 65680,
    "hrpschrd": 3584,
    "jazzgtr": 27712,
    "jingles": 16944,
    "jungle": 13616,
    "kalimba": 2208,
    "kick1": 4544,
    "kick2": 5024,
    "koto": 20832,
    "lead5th": 6464,
    "maracas": 4560,
    "marcato": 61232,
    "marimba": 2064,
    "metalpad": 30288,
    "metbell": 112,
    "metclick": 112,
    "musicbox": 15312,
    "mutegtr": 17008,
    "mutetrum": 9168,
    "nyguitar": 19200,
    "oboe": 3952,
    "ocarina": 1616,
    "odguitar": 12640,
    "orchhit": 14208,
    "percorg": 7520,
    "piccolo": 4320,
    "pickbass": 16416,
    "pistol": 18144,
    "pizzcato": 19888,
    "polysyn": 30224,
    "recorder": 2656,
    "reedorg": 1568,
    "revcym": 13536,
    "rockorg": 30288,
    "santur": 21760,
    "sawwave": 27056,
    "scratch1": 4384,
    "scratch2": 2288,
    "seashore": 31040,
    "shakazul": 31136,
    "shaker": 3104,
    "shamisen": 13136,
    "shannai": 9792,
    "sitar": 18288,
    "slap": 5856,
    "slapbas1": 27872,
    "slapbas2": 20592,
    "slowstr": 18192,
    "snare1": 8544,
    "snare2": 4096,
    "soundtrk": 19888,
    "sprnosax": 7072,
    "sqrclick": 112,
    "sqrwave": 15056,
    "startrak": 27376,
    "steeldrm": 11952,
    "stickrim": 2848,
    "sticks": 4224,
    "surdo1": 9600,
    "surdo2": 9600,
    "sweeper": 31216,
    "synbass1": 6160,
    "synbass2": 2928,
    "synbras1": 30704,
    "synbras2": 30160,
    "synpiano": 5456,
    "synstr1": 31216,
    "synstr2": 16416,
    "syntom": 30512,
    "taiko": 18672,
    "tamborin": 8944,
    "telephon": 4416,
    "tenorsax": 8448,
    "timbaleh": 5264,
    "timbalel": 9728,
    "timpani": 7072,
    "tomhi1": 6576,
    "tomhi2": 6560,
    "tomlo1": 6560,
    "tomlo2": 9600,
    "tommid1": 6560,
    "tommid2": 6560,
    "toms": 6576,
    "tremstr": 61232,
    "triangl1": 2224,
    "triangl2": 15792,
    "trombone": 12896,
    "trumpet": 6608,
    "tuba": 5760,
    "tubebell": 9120,
    "unicorn": 30096,
    "vibes": 10640,
    "vibslap": 9456,
    "viola": 27952,
    "violin": 12160,
    "voices": 14976,
    "voxlead": 14992,
    "warmpad": 18080,
    "whistle": 5872,
    "whistle1": 2000,
    "whistle2": 928,
    "woodblk": 3680,
    "woodblk1": 2352,
    "woodblk2": 3680,
    "woodflut": 1936,
    "xylophon": 9376,
}

# Groups of "similar sounding" instruments. The first instrument in each
# group is the "leader" and will be used as the fallback for other
# instruments in the group if they are not popular enough to be included.
#
# These groups are based on having listened to the instruments in the
# GUS patch set using the generated comparison mid (see comparison.py),
# with similar sounding instruments being grouped together.
#
# If you want to improve the generated config, here's where to start.
# Separating out into more, smaller groups helps, but the 256KB
# config's limited size is quite restrictive. In particular, it's
# important that the "leader" instrument for each group is small
# (see table above of patch sizes).

SIMILAR_GROUPS = [
    # Pianos.
    ("synpiano", "acpiano", "britepno", "honky"),
    ("glocken", "epiano1", "epiano2", "celeste"),
    # Harpsichord sounds noticeably different to pianos:
    ("hrpschrd", "clavinet"),
    # Xylophone etc.
    (
        "marimba",
        "musicbox",
        "vibes",
        "xylophon",
        "tubebell",
        "carillon",
        "santur",
        "kalimba",
    ),
    # Organs.
    ("homeorg", "percorg", "rockorg", "church", "reedorg"),
    # Accordion/Harmonica:
    ("accordn", "harmonca", "concrtna"),
    # Guitars.
    ("nyguitar", "acguitar", "jazzgtr"),
    # Overdriven/distortion guitars sound different. Besides, we
    # definitely want at least one of these.
    ("odguitar", "distgtr", "gtrharm", "cleangtr", "bagpipes"),
    # Basses.
    ("synbass2", "acbass", "fngrbass", "pickbass", "basslead", "fretless"),
    ("synbass1", "slapbas1", "slapbas2", "mutegtr"),
    # Violin and similar string instruments.
    ("violin", "viola", "cello", "contraba", "pizzcato", "harp"),
    # Other stringed (?)
    (
        "synstr2",
        "slowstr",
        "marcato",
        "synstr1",
        "choir",
        "doo",
        "voices",
        "orchhit",
        "polysyn",
        "bowglass",
        "tremstr",
        "fantasia",
        "warmpad",
        "ghostie",
        "metalpad",
        "sweeper",
        "halopad",
    ),
    # Trumpet and other brass.
    (
        "trumpet",
        "trombone",
        "tuba",
        "mutetrum",
        "frenchrn",
        "hitbrass",
        "synbras1",
        "synbras2",
    ),
    # Reed instruments.
    (
        "altosax",
        "sprnosax",
        "tenorsax",
        "barisax",
        "oboe",
        "englhorn",
        "bassoon",
        "clarinet",
    ),
    # Pipe instruments.
    (
        "recorder",
        "flute",
        "piccolo",
        "woodflut",
        "bottle",
        "shakazul",
        "whistle",
        "ocarina",
        "fiddle",
        "shannai",
        "calliope",
        "chiflead",
        "charang",
    ),
    # Leads:
    ("sqrwave", "sawwave", "voxlead", "lead5th"),
    # Odd stringed instruments.
    ("sitar", "banjo", "shamisen", "koto"),
    # Percussion sounds.
    # Kick:
    ("kick2", "taiko", "kick1"),
    # Conga:
    ("congahi2", "congahi1", "congalo"),
    # Snare drums:
    ("snare2", "claps", "snare1"),
    # Toms:
    (
        "tomlo1",
        "toms",
        "syntom",
        "tomlo2",
        "tommid1",
        "tommid2",
        "tomhi2",
        "tomhi1",
        "timpani",
    ),
    # Cymbal crash:
    ("cymsplsh", "cymcrsh2", "cymcrsh1", "revcym", "cymchina"),
    # Cymbal ride:
    ("cymride1", "cymride2", "cymbell", "hihatop"),
    # Hi-hat:
    ("hihatpd", "hihatcl"),
    # Metallic sounding:
    ("bongohi", "bongolo", "timbaleh", "timbalel", "cowbell"),
    # Click:
    ("stickrim", "woodblk1", "woodblk2", "woodblk", "clave"),
    # Random instruments we don't include unless they're popular enough.
    (
        "blank",
        # Special effects:
        "unicorn",
        "soundtrk",
        "aurora",
        "crystal",
        "atmosphr",
        "freshair",
        "echovox",
        "startrak",
        "fx-fret",
        "fx-blow",
        "seashore",
        "jungle",
        "telephon",
        "helicptr",
        "applause",
        "pistol",
        # Percussion:
        "cabasa",
        "whistle1",
        "whistle2",
        "vibslap",
        "maracas",
        "guiro1",
        "guiro2",
        "cuica1",
        "cuica2",
        "steeldrm",
        "agogohi",
        "agogolo",
        "agogo",
        "triangl1",
        "triangl2",
        "tamborin",
    ),
]
