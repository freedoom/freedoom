#!/usr/bin/python

import sys
import gtk
import gtk.glade

class Patch:
	def __init__(self, n,x,y):
		self.name = n
		self.yoff = x
		self.xoff =y

class Texture:
	def __init__(self,name,width,height):
		self.name = name
		self.width = width
		self.height = height
		self.patches = []

def do_nothing(arg):
	print "ZOMG<"

class HellowWorldGTK:
	"""This is an Hello World GTK application"""
	
	def parse_texture_file(self,fname):
		texture1 = file(fname, "r").read()
		self.textures = {}
		textures = self.textures
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

	def set_texture(self, name):
		# parse the example texture, fetch the width,height;
		# create Patch objects and stuff them into a list
		texture = self.textures[name]

		# read the patches into pixbufs
		# a horrid hack to get them client->server side
		for patch in texture.patches:
			self.image1.set_from_file(patch.name.lower() + ".gif")
			patch.pixbuf = self.image1.get_pixbuf()

		texbuf = gtk.gdk.Pixbuf(
			texture.patches[0].pixbuf.get_colorspace(),
			texture.patches[0].pixbuf.get_has_alpha(),
			texture.patches[0].pixbuf.get_bits_per_sample(),
			int(texture.width),
			int(texture.height))

		# copy each patch into the texture pixbuf
		for patch in texture.patches:
			patch.pixbuf.copy_area(0,0,
				patch.pixbuf.get_width(),
				patch.pixbuf.get_height(),
				texbuf, patch.xoff, patch.yoff)

		self.image1.set_from_pixbuf(texbuf)
		
		# scale the texture up
		pixbuf = self.image1.get_pixbuf()
		if pixbuf:
			scale = 2
			self.image1.set_from_pixbuf(pixbuf.scale_simple(
				pixbuf.get_width()  * scale,
				pixbuf.get_height() * scale,
				gtk.gdk.INTERP_NEAREST
			))

	def __init__(self):
		self.gladefile = "cleanroom.glade"
		self.wTree = gtk.glade.XML(self.gladefile,"window1")
		self.image1 = self.wTree.get_widget("orig_texture")
		
		# read in the IWAD texture1 lump and populate our LHS list
		self.parse_texture_file("combined.txt")
		lhs = self.wTree.get_widget("texture_list")
		treestore = gtk.TreeStore(str)
		a = self.textures.keys()
		a.sort()
		for name in a:
			treestore.append(None, [ name ])
		column = gtk.TreeViewColumn('Texture name ')
		lhs.set_model(treestore)
		lhs.append_column(column)
		cell = gtk.CellRendererText()
		column.pack_start(cell, False)
		column.add_attribute(cell, "text", 0)
		lhs.connect("cursor-changed", do_nothing)

		# set the progress bar up
		# by default we've "done" all the 1-patch textures
		bar = self.wTree.get_widget("progressbar1")
		done = len(filter(lambda x: len(x.patches) > 1, self.textures.values()))
		bar.set_fraction(float(done) / len(self.textures))
		bar.set_text("%d/%d" % (done, len(self.textures)))

		self.set_texture("COMPUTE2")

		self.wTree.get_widget("window1").connect("destroy", gtk.main_quit)
		self.wTree.get_widget("quit_menu_item").connect("activate", gtk.main_quit)

if __name__ == "__main__":
	hwg = HellowWorldGTK()
	gtk.main()
