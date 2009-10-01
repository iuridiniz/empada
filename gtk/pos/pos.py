#!/usr/bin/python

from settings import GLADE_FILE, BASE_URL

import pygtk
pygtk.require("2.0")
import gtk  
import gobject

from datetime import datetime

import locale
import gettext
from gettext import gettext as _


import urllib2
import json


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
        self.__setup_sellings__()

    def __setup_clock__(self):
        label_clock = self.builder.get_object("label_clock")
        self.update_clock(label_clock)
        self.gsource_id_update_clock = gobject.timeout_add(1000, self.update_clock, label_clock)
    
    def __setup_window__(self):
        self.window = self.builder.get_object("window_pos")
        self.window.connect("destroy", gtk.main_quit)

    def __setup_sellings__(self):
        b = self.builder.get_object("button_selling_list")
        w = self.builder.get_object("window_selling")

        self.update_sellings()

        self.gsource_id_update_sellings = gobject.timeout_add(2000, self.update_sellings)
        b.connect("clicked", lambda x: w.show())

    def update_sellings(self):
        #print BASE_URL + "Selling/"
        req = urllib2.Request(BASE_URL + "Selling/is_opened/")
        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError:
            sellings = []
        else:
            json_data = response.read()
            sellings = json.loads(json_data)

        label_opened = self.builder.get_object("label_opened")
        label_opened.set_label(_("Opened sellings: %03d") % len(sellings))
        print _("Opened sellings: %03d") % len(sellings)
        return True
        
    def update_clock(self, label_clock=None):
        if label_clock is None:
            label_clock = self.builder.get_object("label_clock")
        now = datetime.now()
        label_clock.set_label("%02d:%02d:%02d" % (now.hour, now.minute, now.second))
        #label_clock.set_label("%02d:%02d:%02d" % (now.hour, now.minute, now.second))
        return True
    

    def main(self):
        self.window.show()
        gtk.main()

if __name__ == "__main__":
    p = Pos()
    p.main()

