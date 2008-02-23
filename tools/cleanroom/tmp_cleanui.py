#!/usr/bin/python

import sys
import gtk
import gtk.glade

from doom import Patch, Texture

class HellowWorldGTK:
	"""This is an Hello World GTK application"""
	
	def parse_texture_file(self,fname):
		texture1 = file(fname, "r").read()
		self.textures = {}
		self.wip_textures = {}
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
				self.wip_textures[line[0]] = Texture(line[0],line[1],line[2])
				textures[line[0]] = current
		# now weed out the 1-patch ones
		keys = self.textures.keys()
		for key in keys:
			if 1 == len(self.textures[key].patches):
				del self.textures[key]
				del self.wip_textures[key]

	def lhs_callback(self, treeview):
		offs,col = treeview.get_cursor()
		# TODO: sanity check the insane subscripting here
		row = treeview.get_model()[offs[0]][0]
		self.set_texture(row)
		# clear out the patch-list for this texture
		selected_patches = self.wTree.get_widget("selected_patches")
		model = selected_patches.get_model()
		model.clear()
		wip_texture = self.wip_textures[row]
		for patch in wip_texture.patches:
			model.append(None, [ patch.name, patch.xoff, patch.yoff ])
			

	def rhs_drag_data_get(self,widget,ctx,selection,targettype,eventtime):
		print "ZOMG"

	# patch selected on rhs
	def rhs_select_cb(self, rhs, path, view_column):
		model = rhs.get_model()
		row = model[path[0]][0]
		selected_patches = self.wTree.get_widget("selected_patches")
		model = selected_patches.get_model()
		model.append(None, [ row, 0, 0 ])
		# redraw the rhs. a bit hacky
		current_texture_name = self.current_texture()
		current_texture = self.wip_textures[current_texture_name]
		current_texture.patches.append(Patch(row,0,0))
		self.init_texture_pixbuf(self.wip_textures[current_texture_name])
		# this redraws the lhs too, unnecessarily
		self.set_texture(current_texture_name)

	def current_texture(self):
		"""return the name of the currently selected texture"""
		lhs = self.wTree.get_widget("texture_list")
		offs,col = lhs.get_cursor()
		lhs_model = lhs.get_model()
		return lhs_model[offs[0]][0]

	def rhs_cursor_cb(self, rhs):
		offs,col = rhs.get_cursor()
		rhs_model = rhs.get_model()
		row = rhs_model[offs[0]][0]
		
		image = self.wTree.get_widget("current_patch")
		image.set_from_file("../../patches/" + row.lower() + ".gif")
		# scale the texture up
		pixbuf = image.get_pixbuf()
		if pixbuf:
			scale = 2
			image.set_from_pixbuf(pixbuf.scale_simple(
				pixbuf.get_width()  * scale,
				pixbuf.get_height() * scale,
				gtk.gdk.INTERP_NEAREST
			))

	def init_texture_pixbuf(self, texture):
		for patch in texture.patches:
			# read the patches into pixbufs
			# a horrid hack to get them client->server side
			image = gtk.Image()
			if not self.patch_pixbufs.has_key(patch.name):
				image.set_from_file("../../patches/" + patch.name.lower() + ".gif")
				pb = image.get_pixbuf()
				self.patch_pixbufs[patch.name] = pb.add_alpha(True,chr(0),chr(255),chr(255))

		texbuf = gtk.gdk.Pixbuf(
			self.patch_pixbufs.values()[0].get_colorspace(),
			self.patch_pixbufs.values()[0].get_has_alpha(),
			self.patch_pixbufs.values()[0].get_bits_per_sample(),
			int(texture.width),
			int(texture.height))

		texbuf.fill(0x00ffffff)
		texbuf = texbuf.add_alpha(True,chr(0),chr(255),chr(255))
		texture.pixbuf = texbuf

		# copy each patch into the texture pixbuf
		for patch in texture.patches:

			dest_x = max(0, patch.xoff)
			dest_y = max(0, patch.yoff)
			dest_height = min(
				self.patch_pixbufs[patch.name].get_height(),
				texbuf.get_height() - dest_y
			)
			dest_width  = min(
				self.patch_pixbufs[patch.name].get_width(),
				texbuf.get_width()  - dest_x
			)
			if patch.xoff < 0:
				dest_width += patch.xoff
			if patch.yoff < 0:
				dest_height += patch.yoff
			offset_x = patch.xoff
			offset_y = patch.yoff
			pb = self.patch_pixbufs[patch.name]
			pb.composite(
				texbuf,
				dest_x, dest_y, dest_width, dest_height,
                offset_x, offset_y, 1, 1, # scale
				gtk.gdk.INTERP_NEAREST, 255)

	def set_texture(self, name):
		# parse the example texture, fetch the width,height;
		# create Patch objects and stuff them into a list
		texture = self.textures[name]
		image = self.wTree.get_widget("orig_texture")

		if not texture.pixbuf:
			self.init_texture_pixbuf(texture)

		image.set_from_pixbuf(texture.pixbuf)
		self.scale_up_texture(image)

		# now for the wip side
		wip_image = self.wTree.get_widget("wip_texture")
		wip_texture = self.wip_textures[name]
		if not wip_texture.pixbuf:
			self.init_texture_pixbuf(wip_texture)
		wip_image.set_from_pixbuf(wip_texture.pixbuf)
		self.scale_up_texture(wip_image)


	def scale_up_texture(self, image):
		# scale the texture up
		pixbuf = image.get_pixbuf()
		if pixbuf:
			scale = 2
			image.set_from_pixbuf(pixbuf.scale_simple(
				pixbuf.get_width()  * scale,
				pixbuf.get_height() * scale,
				gtk.gdk.INTERP_NEAREST
			))
	
	def patch_list_key(self,treeview,event):
		"""handle key press events on the patch list"""
		if gtk.keysyms.Delete == event.keyval:
			offs,col = treeview.get_cursor()
			# remove from data structure
			texture = self.wip_textures[self.current_texture()]
			del texture.patches[offs[0]]
			# remove from UI
			model = treeview.get_model()
			iter = model.get_iter(offs)
			model.remove(iter)
			# redraw RHS
			self.init_texture_pixbuf(texture)
			wip_image = self.wTree.get_widget("wip_texture")
			wip_image.set_from_pixbuf(texture.pixbuf)
			self.scale_up_texture(wip_image)

	def cell_callback(self, cellrenderertext, path, new_text):
		"""cell edited in patch list"""
		current_texture = self.wip_textures[self.current_texture()]
		path = int(path)
		new_text = int(new_text)
		if self.cellrendererwidth == cellrenderertext:
			current_texture.patches[path].xoff = new_text
			column = 1
		else:
			current_texture.patches[path].yoff = new_text
			column = 2
		self.init_texture_pixbuf(current_texture)
		wip_image = self.wTree.get_widget("wip_texture")
		wip_image.set_from_pixbuf(current_texture.pixbuf)
		self.scale_up_texture(wip_image)

		# update the model now
		selected_patches = self.wTree.get_widget("selected_patches")
		model = selected_patches.get_model()
		iter = model.get_iter(path)
		model.set_value(iter, column, new_text)


	def patch_list_reordered(self,treemodel,path,iter,new_order):
		print "ZOMG"


	def __init__(self):
		self.gladefile = "cleanroom.glade"
		self.wTree = gtk.glade.XML(self.gladefile,"window1")
		self.image1 = self.wTree.get_widget("orig_texture")
		
		window = self.wTree.get_widget("window1")
		window.resize(1024,768)

		self.patch_pixbufs = {}
		
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

		# prepare the patch list
		patch_list = self.wTree.get_widget("selected_patches")
		treestore = gtk.TreeStore(str,int,int)
		column = gtk.TreeViewColumn('Patch name')
		patch_list.set_model(treestore)
		patch_list.append_column(column)
		cell = gtk.CellRendererText()
		column.pack_start(cell, False)
		column.add_attribute(cell, "text", 0)

		cell = gtk.CellRendererText()
		self.cellrendererwidth = cell
		cell.set_property("editable", True)
		cell.connect("edited", self.cell_callback)
		column = gtk.TreeViewColumn('X offset')
		patch_list.append_column(column)
		column.pack_start(cell, False)
		column.add_attribute(cell, "text", 1)

		cell = gtk.CellRendererText()
		cell.set_property("editable", True)
		cell.connect("edited", self.cell_callback)
		column = gtk.TreeViewColumn('Y offset')
		patch_list.append_column(column)
		column.pack_start(cell, False)
		column.add_attribute(cell, "text", 2)

		patch_list.connect("key-press-event", self.patch_list_key)
		patch_list.set_reorderable(True)
		treestore.connect("rows-reordered", self.patch_list_reordered)

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
		rhs.connect("cursor-changed", self.rhs_cursor_cb)
		rhs.connect("row-activated", self.rhs_select_cb)

		image = self.wTree.get_widget("current_patch")
		image.drag_source_set(gtk.gdk.BUTTON1_MASK, [('text/plain', 0,
			80)], 0) # 80 = target type text
		image.connect("drag_data_get", self.rhs_drag_data_get)

		self.set_up_progressbar()

		self.wTree.get_widget("window1").connect("destroy", gtk.main_quit)
		self.wTree.get_widget("quit_menu_item").connect("activate", gtk.main_quit)
		self.wTree.get_widget("saveas_menu_item").connect("activate", self.saveas_activated)
		self.wTree.get_widget("save_menu_item").connect("activate", self.save_activated)
		self.wTree.get_widget("open_menu_item").connect("activate", self.open_activated)

		# select the top-most texture
		lhs.set_cursor( (0,) , None, False)

	def set_up_progressbar(self):
		"""We've "done" any textures in wip set with >0 patches"""
		bar = self.wTree.get_widget("progressbar1")
		done = len(filter(lambda x: len(x.patches) > 0, self.wip_textures.values()))
		bar.set_fraction(float(done) / len(self.textures))
		bar.set_text("%d/%d" % (done, len(self.textures)))

	def saveas_activated(self, arg):
		filesel = gtk.FileChooserDialog(action=gtk.FILE_CHOOSER_ACTION_SAVE,
			buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
				gtk.STOCK_SAVE, gtk.RESPONSE_OK))
		if filesel.run() == gtk.RESPONSE_OK:
			self.filename = filesel.get_filename()
		filesel.destroy()
		self.save_activated(arg)

	def save_activated(self, arg):
		if not hasattr(self, "filename"):
			self.saveas_activated(arg)
		saveme = self.wip_textures.values()
		saveme.sort(lambda a,b: cmp(a.name,b.name))
		writetome = open(self.filename,"w")
		writetome.write("".join(map(str,saveme)))
		writetome.close()

	def open_activated(self,arg):
		filesel = \
		gtk.FileChooserDialog(action=gtk.FILE_CHOOSER_ACTION_OPEN,
			buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
				gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		if filesel.run() == gtk.RESPONSE_OK:
			self.filename = filesel.get_filename()
		filesel.destroy()
		print self.filename
		
		texture1 = file(self.filename, "r").read()
		self.wip_textures = {}
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
				self.wip_textures[line[0]] = current
		self.set_up_progressbar()

if __name__ == "__main__":
	hwg = HellowWorldGTK()
	gtk.main()
