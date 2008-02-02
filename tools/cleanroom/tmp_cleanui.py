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

	def lhs_callback(self, treeview):
		offs,col = treeview.get_cursor()
		# TODO: sanity check the insane subscripting here
		row = treeview.get_model()[offs[0]][0]
		self.set_texture(row)

	def rhs_callback(self, rhs):
		offs,col = rhs.get_cursor()
		rhs_model = rhs.get_model()
		row = rhs_model[offs[0]][0]
		
		image = self.wTree.get_widget("current_patch")
		image.set_from_file("../../patches/" + row.lower() + ".gif")

	def set_texture(self, name):
		# parse the example texture, fetch the width,height;
		# create Patch objects and stuff them into a list
		texture = self.textures[name]
		print "composing texture %s (%dx%d)\n" % \
			(name,int(texture.width),int(texture.height))

		# read the patches into pixbufs
		# a horrid hack to get them client->server side
		for patch in texture.patches:
			self.image1.set_from_file("../../patches/" + patch.name.lower() + ".gif")
			patch.pixbuf = self.image1.get_pixbuf()

		texbuf = gtk.gdk.Pixbuf(
			texture.patches[0].pixbuf.get_colorspace(),
			texture.patches[0].pixbuf.get_has_alpha(),
			texture.patches[0].pixbuf.get_bits_per_sample(),
			int(texture.width),
			int(texture.height))

		# copy each patch into the texture pixbuf
		for patch in texture.patches:
			print "about to copy patch %s (%d,%d) to (%d,%d)"% \
				( patch.name, patch.pixbuf.get_width(),
				patch.pixbuf.get_height(),
				patch.xoff, patch.yoff
				)
			# top-left coords of source
			src_x = max(-1 * patch.xoff, 0)
			src_y = max(-1 * patch.yoff, 0)
			# amount to copy
			width = patch.pixbuf.get_width()
			if width + patch.xoff > int(texture.width):
				print "patch too wide, shortening"
				width = int(texture.width) - patch.xoff
			height = patch.pixbuf.get_height()
			if height + patch.yoff > int(texture.height):
				print "patch too high, shortening"
				height = min(int(texture.height), int(texture.height) - patch.yoff)
			print "debug: src x/y = %d,%d; w/h = %d,%d" % (src_x,src_y,width,height)
			dest_xoff = max(0, patch.xoff)
			dest_yoff = max(0, patch.yoff)
			patch.pixbuf.copy_area( src_x, src_y, width, height, texbuf, dest_xoff, dest_yoff)

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
		self.parse_texture_file("../../textures/combined.txt")
		lhs = self.wTree.get_widget("texture_list")
		treestore = gtk.TreeStore(str)
		tmp_texnames = self.textures.keys()
		tmp_texnames.sort()
		for name in tmp_texnames:
			if len(self.textures[name].patches) > 1:
				treestore.append(None, [ name ])
		column = gtk.TreeViewColumn('Texture name ')
		lhs.set_model(treestore)
		lhs.append_column(column)
		cell = gtk.CellRendererText()
		column.pack_start(cell, False)
		column.add_attribute(cell, "text", 0)
		lhs.connect("cursor-changed", self.lhs_callback)

		# select the top-most item
		lhs.set_cursor( (0,) , None, False)

		# prepare the patch list
		patch_list = self.wTree.get_widget("selected_patches")
		treestore = gtk.TreeStore(str)
		column = gtk.TreeViewColumn('Patch name')
		patch_list.set_model(treestore)
		patch_list.append_column(column)
		cell = gtk.CellRendererText()
		column.pack_start(cell, False)
		column.add_attribute(cell, "text", 0)

		# populate the RHS list with patch names
		# yes, I learnt perl once.
		patches = {}
		for texture in self.textures.values():
			for patch in texture.patches:
				patches[patch.name] = 1
		patches = patches.keys()
		rhs = self.wTree.get_widget("all_patch_tree")
		treestore = gtk.TreeStore(str)
		patches.sort()
		for name in patches:
			treestore.append(None, [ name ])
		column = gtk.TreeViewColumn('Patch name')
		rhs.set_model(treestore)
		rhs.append_column(column)
		cell = gtk.CellRendererText()
		column.pack_start(cell, False)
		column.add_attribute(cell, "text", 0)
		rhs.connect("cursor-changed", self.rhs_callback)

		# set the progress bar up
		# by default we've "done" all the 1-patch textures
		bar = self.wTree.get_widget("progressbar1")
		done = len(filter(lambda x: len(x.patches) > 1, self.textures.values()))
		bar.set_fraction(float(done) / len(self.textures))
		bar.set_text("%d/%d" % (done, len(self.textures)))

		self.wTree.get_widget("window1").connect("destroy", gtk.main_quit)
		self.wTree.get_widget("quit_menu_item").connect("activate", gtk.main_quit)

if __name__ == "__main__":
	hwg = HellowWorldGTK()
	gtk.main()
