#!/usr/bin/env python
# coding: utf-8

import cgi
import cgitb; cgitb.enable()
import sys
import urllib
from django.http import HttpResponse

def get_result(host):
        wp = urllib.urlopen(url='http://'+host+':18000/result.html')
        gwp = wp.read()
        return gwp

def start(req):
	form = req.GET
	return HttpResponse(get_result(form['ip']))

if __name__ == '__main__':
	argvs = sys.argv
	print get_result(argvs[1])

