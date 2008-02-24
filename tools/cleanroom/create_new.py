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

oldtex = file("../../textures/combined.txt", "r").read()
patches = []
texline = ''
for line in oldtex.split("\n"):
	# start of a patch line
	if len(line) > 0 and line[0] == "*":
		patches.append(line)
	else:
		# end of a texture definition and we had just one patch
		if 1 == len(patches):
			print patches[0]
			patches = []
			texline = ''
		# end of a texture definition,look up the patches
		elif texline != '':
			bits = texline.split()
			if bits[0] in textures:
				texture = textures[bits[0]]
				print '\n'.join(map(str,texture.patches))
				texline = ''
			else:
				sys.stderr.write("uh oh, no idea of patches for %s"%bits[0])

		# start of a texture definition
		if re.match(r'^[A-Z]', line):
			texline = line
		print line
