#!/usr/bin/python

from os.path import realpath, dirname, sep

BASEDIR=realpath(dirname(__file__)) + sep

APPNAME="empada"

GLADE_FILE=BASEDIR + "pos.glade"

BASE_URL="http://localhost:8000/pos/json/"

