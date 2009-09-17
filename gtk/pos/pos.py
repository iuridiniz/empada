#!/usr/bin/python


import pygtk
pygtk.require("2.0")
import gtk  
import gobject

from datetime import datetime

import locale
import gettext
from gettext import gettext as _


GLADE_FILE="pos.glade"
CLOCK_SIZE="24000" # 24 pts * 1000



#class Token:
#    def __init__(self, builder=None, ticket_number=-1):
#        if builder == None:
#            self.builder = gtk.Builder()
#            self.builder.add_from_file(GLADE_FILE)
#        else:
#            self.builder = builder
#
#        self.window = self.builder.get_object("window_token")
#
#    def show(self):
#        self.window.show()
#    
#    def hide(self):
#        self.window.hide()
    

class Pos:
    def __init__(self):
        self.builder = gtk.Builder()
        #self.builder.set_translation_domain("pos")
        self.builder.add_from_file(GLADE_FILE)
        self.__setup_clock__()
        self.__setup_window__()
        self.__setup_tokens__()

    def __setup_clock__(self):
        label_clock = self.builder.get_object("label_clock")
        self.update_clock(label_clock)
        self.gsource_id_update_clock = gobject.timeout_add(1000, self.update_clock, label_clock)
    
    def __setup_window__(self):
        self.window = self.builder.get_object("window_pos")
        self.window.connect("destroy", gtk.main_quit)

    def __setup_tokens__(self):
        b = self.builder.get_object("button_ticketlist")
        w = self.builder.get_object("window_ticket")
        b.connect("clicked", lambda x: w.show())

    def update_clock(self, label_clock):
        now = datetime.now()
        label_clock.set_label("<span size='%s'>%02d:%02d:%02d</span>" % (CLOCK_SIZE, now.hour, now.minute, now.second))
        #label_clock.set_label("%02d:%02d:%02d" % (now.hour, now.minute, now.second))
        return True
    

    def main(self):
        self.window.show()
        gtk.main()

if __name__ == "__main__":
    p = Pos()
    p.main()

