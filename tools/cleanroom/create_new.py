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
for line in oldtex.split("\n"):
	if len(line) == 0 or line[0] == ";" or line[0] == "#":
		print line
	elif line[0] == "*":
		patches.append(line)
	else:
		if 1 == len(patches):
			print patches[0]
		patches = []
		print line
