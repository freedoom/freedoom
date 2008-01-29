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

class HellowWorldGTK:
	"""This is an Hello World GTK application"""
	
	example_texture = """COMPUTE2                256     56
*       COMP02_1        0       0
*       COMP02_2        64      0
*       COMP02_3        128     0
*       COMP02_7        192     0"""

	def parse_texture_file(self,fname):
		texture1 = file(fname, "r").read()
		self.textures = []
		textures = self.textures
		current = None
		for line in texture1.split("\n"):
			if len(line) == 0 or line[0] == ";" or line[0] == "#":
				continue
			elif line[0] == "*" and current:
				current.patches.append(line)
			else:
				line = line.split()
				if len(line) != 3:
					print "OH CRAP"
					print line
				current = Texture(line[0],line[1],line[2])
				textures.append(current)
	
	def __init__(self):
		self.gladefile = "cleanroom.glade"
		self.wTree = gtk.glade.XML(self.gladefile,"window1")
		self.image1 = self.wTree.get_widget("orig_texture")
		
		# read in the IWAD texture1 lump and populate our LHS list
		self.parse_texture_file("combined.txt")
		lhs = self.wTree.get_widget("texture_list")
		treestore = gtk.TreeStore(str)
		for texture in self.textures:
			treestore.append(None, [ texture.name ])
		column = gtk.TreeViewColumn('Texture name ')
		lhs.set_model(treestore)
		lhs.append_column(column)
		cell = gtk.CellRendererText()
		column.pack_start(cell, False)
		column.add_attribute(cell, "text", 0)

		# set the progress bar up
		# by default we've "done" all the 1-patch textures
		bar = self.wTree.get_widget("progressbar1")
		done = len(filter(lambda x: len(x.patches) > 1, self.textures))
		bar.set_fraction(float(done) / len(self.textures))
		bar.set_text("%d/%d" % (done, len(self.textures)))

		# parse the example texture, fetch the width,height;
		# create Patch objects and stuff them into a list
		patches = []
		width,height = 0,0
		for line in self.example_texture.split("\n"):
			if len(line) > 0:
				# texture definition (we hope)
				if line[0] != '*':
					name,width,height = line.split()
				# patch list (we hope)
				else:
					junk,name,y,x= line.split()
					patches.append(Patch(name,int(x),int(y)))
		
		# read the patches into pixbufs
		# a horrid hack to get them client->server side
		for patch in patches:
			self.image1.set_from_file(patch.name.lower() + ".gif")
			patch.pixbuf = self.image1.get_pixbuf()
		
		texbuf = gtk.gdk.Pixbuf(
			patches[0].pixbuf.get_colorspace(),
			patches[0].pixbuf.get_has_alpha(),
			patches[0].pixbuf.get_bits_per_sample(),
			int(width),
			int(height))

		# copy each patch into the texture pixbuf
		for patch in patches:
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
		
		self.wTree.get_widget("window1").connect("destroy", gtk.main_quit)
		self.wTree.get_widget("quit_menu_item").connect("activate", gtk.main_quit)

if __name__ == "__main__":
	hwg = HellowWorldGTK()
	gtk.main()
