#!/usr/bin/env python
# coding: utf-8

import os
import sys
import cgi
import cgitb; cgitb.enable()
import urllib
import commands
from string import Template
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/../../scripts')
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import log

@csrf_exempt
def start(req):
	base_path = os.path.abspath(os.path.dirname(__file__))
	form = req.GET
	ret = commands.getoutput('sudo ip netns exec ' + urllib.unquote(form['netns']) + ' /usr/bin/python '
		 + base_path + '/scenario_result.py ' + urllib.unquote(form['ip']))
	return HttpResponse(ret)
