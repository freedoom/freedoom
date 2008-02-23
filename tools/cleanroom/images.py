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

    # is invoked when the button is clicked.  It just prints a message.
    def button_clicked(self, widget, data=None):
        print "button %s clicked" % data

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
        image = gtk.Image()
        image.set_from_file("../../patches/wall40_1.gif")
        image.show()
        # a button to contain the image widget
        button = gtk.Button()
        button.add(image)
        button.show()
        hbox.pack_start(button)
        button.connect("clicked", self.button_clicked, "2")

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    ImagesExample()
    main()
