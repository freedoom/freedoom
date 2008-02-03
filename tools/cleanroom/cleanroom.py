#!/usr/bin/python

# cleanroom.py: a clean-room IWAD texture1 lump constructor
from doom import Patch, Texture

class Model:
	"""The Model represents the original texture list,
		the WIP texture list, and various bits of state.
	"""
	def parse_texture_file(self,fname):
		texture1 = file(fname, "r").read()
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
		return textures

	def new_wip_textures(self):
		for texture in self.orig_textures.values():
			self.wip_textures[texture.name] = \
				Texture(texture.name, texture.width, texture.height)

	def __init__(self):
		self.orig_textures = \
			self.parse_texture_file("../../textures/combined.txt")
		self.wip_textures = {}

model = Model()
print "\n\n\torig\n\n"
print "".join(map(str, model.orig_textures.values()))

print "\n\n\tnew\n\n"
model.new_wip_textures()
print "".join(map(str, model.wip_textures.values()))
