#!/usr/bin/env python

# example images.py

import pygtk
pygtk.require('2.0')
import gtk

class ImagesExample:
    # when invoked (via signal delete_event), terminates the application.
    def close_application(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def __init__(self):
        # create the main window, and attach delete_event signal to terminating
        # the application
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.connect("delete_event", self.close_application)
        window.set_border_width(10)
        window.show()

        # a horizontal box to hold the buttons
        hbox = gtk.HBox()
        hbox.show()
        window.add(hbox)

        # create several images with data from files and load images into
        # buttons
        baseimage = gtk.Image()
        baseimage.set_from_file("../../patches/wall40_1.gif")
        pixbuf = baseimage.get_pixbuf()
        if pixbuf:
            scale = 1
            baseimage.set_from_pixbuf(pixbuf.scale_simple(
                pixbuf.get_width()  * scale,
                pixbuf.get_height() * scale,
                gtk.gdk.INTERP_NEAREST
            ))
        baseimage.show()

        basepatch = gtk.Image()
        basepatch.set_from_file("../../patches/ps20a0.gif")
        pb = basepatch.get_pixbuf()
        basepatch.set_from_pixbuf(pb.scale_simple(
            pb.get_width()  * scale,
            pb.get_height() * scale,
            gtk.gdk.INTERP_NEAREST
        ))
        pb = basepatch.get_pixbuf()
        pb = pb.add_alpha(True,chr(0),chr(255),chr(255))

        for x,y in [(0,0), (24,24), (104,16), (24,104), (-16,0), (0,-16)]:
            x *= scale
            y *= scale
            image = gtk.Image()
            image.set_from_pixbuf(baseimage.get_pixbuf().copy())
            image.show()

            dest_x = max(0, x)
            dest_y = max(0, y)
            dest_height = min(pb.get_height(), image.get_pixbuf().get_height() - dest_y)
            dest_width  = min(pb.get_width(),  image.get_pixbuf().get_width()  - dest_x)
            if x < 0:
                dest_width += x
            if y < 0:
                dest_height += y
            offset_x = x
            offset_y = y

            pb.composite(
                image.get_pixbuf(),
                dest_x, dest_y, dest_width, dest_height,
                offset_x, offset_y, 1, 1, # scale
                gtk.gdk.INTERP_NEAREST, 255
            )

            # a button to contain the image widget
            button = gtk.Button()
            button.add(image)
            button.show()
            hbox.pack_start(button)

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    ImagesExample()
    main()
