#!/usr/bin/python


from settings import BASEDIR, APPNAME

import locale
import gettext
import gtk.glade

APPNAME="empada"
DIR=BASEDIR + "locale"

locale.setlocale(locale.LC_ALL, '')
gtk.glade.bindtextdomain(APPNAME, DIR)
gtk.glade.textdomain(APPNAME)
gettext.bindtextdomain(APPNAME, DIR)
gettext.textdomain(APPNAME)


import pos


if __name__ == "__main__":
    p = pos.Pos()
    p.main()

