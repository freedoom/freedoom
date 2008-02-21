#!/usr/bin/python

from doom import Patch, Texture
import sys,re

if len(sys.argv) != 2:
	sys.stderr.write("usage: sw1_sw2.py <infile>\n")
	sys.exit()

infile = sys.argv[1]

# TODO: a generalized form of this para should probably be moved into the
# Texture class
texture1 = file(infile, "r").read()
textures = {}
current = None
for line in texture1.split("\n"):
	if len(line) == 0 or line[0] == ";" or line[0] == "#":
		continue
	elif line[0] == "*" and current:
		junk,name,y,x= line.split()
		current.patches.append(Patch(name,int(x),int(y)))
	else:
		line = line.split()
		current = Texture(line[0],line[1],line[2])
		textures[line[0]] = current

# a list of known switch textures
switches = {
	"SW1S0": "SW1S1",
	"SW2_1": "SW2_2",
	"SW2_3": "SW2_4",
	"SW2_5": "SW2_6",
	"SW2_7": "SW2_8",
	"SW2S0": "SW2S1",
	"SW3S0": "SW3S1",
	"SW4S0": "SW4S1"
}
# include the opposites
switches.update(dict([ (v,k) for k,v in switches.items() ]))

for sw1 in [x for x in textures.values() if re.match("^SW1", x.name)]:
	sw2n = sw1.name.replace("SW1","SW2")
	if not textures.has_key(sw2n):
		sys.stderr.write("error: %s not defined, skipping\n" % sw2n)
		continue
	sw2 = textures[sw2n]
	if len(sw2.patches) != 0:
		sys.stderr.write("error: %s has patches (%s)\n" % \
			(sw2.name, map(lambda x: x.name,sw2.patches)))
		continue

	# now the magic happens
	for patch in sw1.patches:
		name = patch.name
		if switches.has_key(patch.name):
			name = switches[patch.name]
		sw2.patches.append(Patch(name, patch.yoff,patch.xoff))
	textures[sw2n] = sw2

a = textures.values()
a.sort(lambda a,b: cmp(a.name,b.name))
sys.stdout.write(''.join(map(str,a)))
