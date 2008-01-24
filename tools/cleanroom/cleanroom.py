#!/usr/bin/python

# cleanroom.py: a clean-room IWAD texture1 lump constructor

from sys import argv, exit
from os import rmdir, mkdir, system, chdir, getcwd
from tempfile import mkdtemp

if len(argv) != 2:
	print "usage: cleanroom.py IWAD"
	exit(1)

if system("which deutex >/dev/null"):
	print "you need to install deutex in the PATH"
	exit(1)

iwad = argv[1]
origdir = getcwd()

if iwad[0] != "/":
	iwad = origdir + "/" + iwad

tmpdir = mkdtemp()
chdir(tmpdir)

system("deutex -textures -extract " +iwad + " >/dev/null 2>&1")
system("deutex -patches -extract " +iwad + " >/dev/null 2>&1")

# parse the textures data

texture1 = file(tmpdir + "/textures/texture1.txt", "r").read()

class Texture:
	def __init__(self,name,width,height):
		self.name = name
		self.width = width
		self.height = height
		self.patches = []

textures = []
current = None
for line in texture1.split("\n"):
	if len(line) == 0 or line[0] == ";":
		continue
	elif line[0] == "*" and current:
		current.patches.append(line)
	else:
		line = line.split()
		current = Texture(line[0],line[1],line[2])
		textures.append(current)

# we are not interested in 1-patch textures
textures = filter(lambda x: len(x.patches) > 1, textures)
print len(textures)

chdir(origdir)
rmdir(tmpdir)
