#!/usr/bin/python

from settings import GLADE_FILE, BASE_URL
from utils import logging

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

        self.status_hide_id = 0
        self.opened_sellings_count = -1
        self.closed_sellings_count = -1
        self.opened_sellings = []
        self.closed_sellings = []

        self.__setup_widgets__()
        self.__setup_updates__()

        self.update_sellings()
        self.update_sellings_widgets()
   
        self.flash(_("Welcome to EMPADA 0.1"))
    def __setup_widgets__(self):
        """
        Sets all gtk stuff
        """
        self.__setup_clock_widget__()
        self.__setup_sellings_widgets__()

        # window widget
        self.window = self.builder.get_object("window_pos")
        self.window.connect("destroy", gtk.main_quit)

    def __setup_clock_widget__(self):
        label_clock = self.builder.get_object("label_clock")
        self.update_clock_widget(label_clock)
        self.gsource_id_update_clock = gobject.timeout_add(1000, self.update_clock_widget, label_clock)

    def __setup_sellings_widgets__(self):
        b = self.builder.get_object("button_selling_list")
        #w = self.builder.get_object("window_selling")

        c = self.builder.get_object("combo_selling_list")


        # if not custom ticket clear the combo_box_entry on focus
        clear = lambda *args: c.get_active() != -1 and c.child.set_text("")
        c.child.connect("focus-in-event", clear)
        #c.child.connect("changed", clear)
        #c.child.set_override_mode(True)

        # on enter simulate click on button
        click = lambda *args: b.clicked()
        c.child.connect("activate", click)

        # setup behavior to click
        b.connect("clicked", self.on_button_selling_list_clicked, c)

    def flash(self, message):
        if self.status_hide_id:
            gobject.source_remove(self.status_hide_id)
            self.status_hide_id = 0
        s = self.builder.get_object("status")
        s.show()
        s.push(0, message)
        self.status_hide_id = gobject.timeout_add(3000, self.hide_flash, s)

    def hide_flash(self, status):
        status.hide()
        self.status_hide_id = 0
        return False
            
    def on_button_selling_list_clicked(self, widget, combo_selling_list):
        if combo_selling_list.get_active() == -1:
            logging.info("Getting ticket:" + combo_selling_list.get_active_text())
        else:
            s_id, ticket_id = self.opened_sellings[combo_selling_list.get_active()]
            logging.info("Getting selling:" + str(s_id))


    def __setup_updates__(self):
        self.gsource_id_update_sellings = gobject.timeout_add(2000, self.update_sellings)

    def call_remote(self, url):
        req = urllib2.Request(url)
        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError:
            result = None
            logging.error("Error while requesting: " + url)
            self.flash(_("Cannot connect to server"))
        else:
            json_data = response.read()
            result = json.loads(json_data)
        return result

        
    def update_sellings_widgets(self):
        label_opened = self.builder.get_object("label_opened")
        label_closed = self.builder.get_object("label_closed")
        combo_selling_list = self.builder.get_object("combo_selling_list")
    
        if self.opened_sellings_count == -1:
            label_opened.set_label(_("Opened sellings: %03d") % (0))
        else:
            label_opened.set_label(_("Opened sellings: %03d") % (self.opened_sellings_count,))

        if self.closed_sellings_count == -1:
            label_closed.set_label(_("Closed sellings: %03d") % (0))
        else:
            label_closed.set_label(_("Closed sellings: %03d") % (self.closed_sellings_count,))

        if combo_selling_list.get_model() is None:
            liststore = gtk.ListStore(str)
            combo_selling_list.set_model(liststore)
            #cell = gtk.CellRendererText()
            #combo_selling_list.pack_start(cell, True)
            #combo_selling_list.add_attribute(cell, 'text', 0) 
            combo_selling_list.set_text_column(0)

        combo_selling_list.get_model().clear()

        for i in self.opened_sellings:
            if i[1] == None:
                combo_selling_list.append_text(_("Selling Number %03d") % (i[0],))
            else:
                combo_selling_list.append_text(_("Ticket: %03d | Selling Number %03d") % (i[1], i[0],))

    def update_sellings(self):
        #print BASE_URL + "Selling/"
        url_opened_sellings_count = BASE_URL + "Selling/is_opened/count/"
        url_closed_sellings_count = BASE_URL + "Selling/is_closed/count/"
        url_opened_sellings = BASE_URL + "Selling/is_opened/"
        url_closed_sellings = BASE_URL + "Selling/is_closed/"
       
        update_interface = False
        # opened sellings
        result = self.call_remote(url_opened_sellings_count)
        if result:
            if self.opened_sellings_count != result[0]['result']:
                logging.info("Updating opened selling count to:" + str(result[0]['result']))
                self.opened_sellings_count = result[0]['result']
                
                result = self.call_remote(url_opened_sellings)
                self.opened_sellings = []
                for i in result:
                    self.opened_sellings.append((i['pk'], i['fields']['ticket']))

                logging.info("Current opened sellings: " + str(self.opened_sellings))
                update_interface = True

        # closed sellings
        result = self.call_remote(url_closed_sellings_count)
        if result:
            if self.closed_sellings_count != result[0]['result']:
                logging.info("Updating closed selling count to:" + str(result[0]['result']))
                self.closed_sellings_count = result[0]['result']
                
                result = self.call_remote(url_closed_sellings)
                self.closed_sellings = []
                for i in result:
                    self.closed_sellings.append((i['pk'], i['fields']['ticket']))

                logging.info("Current closed sellings: " + str(self.closed_sellings))
                update_interface = True

        
        if update_interface:
            self.update_sellings_widgets()
        return True
        
    def update_clock_widget(self, label_clock=None):
        if label_clock is None:
            label_clock = self.builder.get_object("label_clock")
        now = datetime.now()
        label_clock.set_label("%02d:%02d:%02d" % (now.hour, now.minute, now.second))
        return True
    
    def main(self):
        self.window.show()
        gtk.main()

if __name__ == "__main__":
    p = Pos()
    p.main()

