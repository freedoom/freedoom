#!/usr/bin/python

import sys
import gtk
import gtk.glade

class Patch:
	def __init__(self, n,w,h):
		self.name = n
		self.width = w
		self.height =h

class HellowWorldGTK:
	"""This is an Hello World GTK application"""
	
	example_texture = """COMPUTE2                256     56
*       COMP02_1        0       0
*       COMP02_2        64      0
*       COMP02_3        128     0
*       COMP02_7        192     0"""
	
	def __init__(self):
		self.gladefile = "cleanroom.glade"
		self.wTree = gtk.glade.XML(self.gladefile,"window1")
		self.image1 = self.wTree.get_widget("orig_texture")
		
		# parse the example texture
		patches = []
		width,height = 0,0
		for line in self.example_texture.split("\n"):
			if len(line) > 0:
				if line[0] != '*':
					name,width,height = line.split()
				else:
					junk,name,width,height = line.split()
					patches.append(Patch(name,width,height))
		
		for patch in patches:
			self.image1.set_from_file(patch.name.lower() + ".gif")
			patch.pixbuf = self.image1.get_pixbuf()
		
		self.image1.set_from_file("comp02_1.gif")
		pixbuf = self.image1.get_pixbuf()
		if pixbuf:
			scale = 3
			self.image1.set_from_pixbuf(pixbuf.scale_simple(
				pixbuf.get_width()  * scale,
				pixbuf.get_height() * scale,
				gtk.gdk.INTERP_NEAREST
			))
		
		self.wTree.get_widget("window1").connect("destroy", gtk.main_quit)

if __name__ == "__main__":
	hwg = HellowWorldGTK()
	gtk.main()
