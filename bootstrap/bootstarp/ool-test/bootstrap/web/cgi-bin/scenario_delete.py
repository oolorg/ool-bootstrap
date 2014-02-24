#!/usr/bin/env python
# coding: utf-8

import cgi
import cgitb; cgitb.enable()
import sys
import threading
import shlex
import time
import subprocess
import os
from string import Template
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/../../scripts')
import log

def exec_release(scid, lbaas):
	script_path = os.path.abspath(os.path.dirname(__file__))
	command = "sudo /usr/bin/python " + script_path + "/../../scripts/release.py " + scid
	if lbaas:
		command += " " + lbaas
	try:
        	log.info("Start to delete id : " + scid)
        	subprocess.Popen(shlex.split(command))
	except OSError as e:
        	log.error( str(type(e)) + str(e.args) + e.message)
        	sys.exit(1)
@csrf_exempt
def start(req):
	form = req.GET
	if not form.has_key('scid'):
		log.error("Not found Parametor scenario-id.")
		sys.exit(1)
	lbaas = ''
	if form.has_key('lbaas') and form['lbaas'] == 'True':
		lbaas = 'lbaas'
	exec_release(form['scid'], lbaas)
	with open(os.path.abspath(os.path.dirname(__file__)) + '/../template/redirect.tmpl') as f:
		data=f.read()
		tmpl=Template(unicode(data, 'utf-8', 'ignore'))
		body=tmpl.substitute({'url':'index.py'})
		return HttpResponse(body)

