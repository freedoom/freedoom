#!/usr/bin/python

import sys
import gtk
import gtk.glade

class HellowWorldGTK:
	"""This is an Hello World GTK application"""
	def __init__(self):
		self.gladefile = "cleanroom.glade"
		self.wTree = gtk.glade.XML(self.gladefile,"window1")
		
		self.image1 = self.wTree.get_widget("orig_texture")
		self.image1.set_from_file("sw2_1.gif")
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
