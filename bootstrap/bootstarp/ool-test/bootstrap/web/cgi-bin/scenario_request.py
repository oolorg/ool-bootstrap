#!/usr/bin/env python
# coding: utf-8

import cgi
import cgitb; cgitb.enable()
import sys
import urllib

def get_result(address):
        wp = urllib.urlopen(url='http://' + address  + ':18000')
        gwp = wp.read()
        return gwp

argvs = sys.argv
print 'Content-Type:text/html'
print get_result(argvs[1])
