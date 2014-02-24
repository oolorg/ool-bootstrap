#!/usr/bin/env python
# coding: utf-8

import os
import sys
import cgi
import cgitb; cgitb.enable()
from django.http import HttpResponse


def start(req):
	form = req.GET
	scid = form['scid']
	log_path = os.path.abspath(os.path.dirname(__file__)) + '/../../logs/' + scid
	result = "<html><body>"
	result += """<table border="0"><tr><td style="width:60em; word-break:break-all;">"""
	with open(log_path) as f:
		for line in f:
			result += line + "<br>"
	result += "</td></tr></table>"
	result += "</body></html>"
	return HttpResponse(result)

