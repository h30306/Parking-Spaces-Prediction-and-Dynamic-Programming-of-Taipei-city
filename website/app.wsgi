#!/usr/bin/python3.6
import os,sys


sys.path.insert(0, '/var/www/html/website')

from server import app as application
application.secret_key = "123"
