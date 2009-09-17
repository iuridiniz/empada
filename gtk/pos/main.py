#!/usr/bin/python

import locale
import gettext
import gtk.glade

APP="empada"
DIR="locale"

locale.setlocale(locale.LC_ALL, '')
gtk.glade.bindtextdomain(APP, DIR)
gtk.glade.textdomain(APP)
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)


import pos


if __name__ == "__main__":
    p = pos.Pos()
    p.main()

