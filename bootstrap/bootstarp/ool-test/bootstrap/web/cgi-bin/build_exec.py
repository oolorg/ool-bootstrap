#!/usr/bin/env python 
# coding: utf-8

import os
import sys
import uuid
import cgi
import pwd
import cgitb; cgitb.enable()
import threading
import subprocess
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from string import Template
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/../../scripts')
import common.credentials as credentials 
import log

def exec_build(scenario, scid):
	script_path = os.path.abspath(os.path.dirname(__file__))
	log_path = "%s/../../logs/%s" % (script_path, scid)
	exe_path = "%s/../../scripts/bootstrap.py" % script_path
	log.debug(exe_path)
	try:
	        f=open(log_path, "w")
	except IOError as e:
	        log.error("can not open :" + log_path)
	        log.error( str(type(e)) + str(e.args) + e.message)
	        sys.exit(1)

	try:
	        log.info("Start to Build scenario : '%s',  uuid : '%s'" % (scenario, scid))
	        subprocess.Popen(['sudo', '/usr/bin/python', exe_path, scid, scenario, 'credentials'], stdout=f, stderr=f)
	except OSError as e:
	        log.error( str(type(e)) + str(e.args) + str(e.message) )
	        sys.exit(1)

@csrf_exempt
def start(req):
	form = req.POST
	if not form.has_key('scenario'):
		log.error("Not found Parametor scenario.")
		sys.exit(1)

	exec_build(form['scenario'], str(uuid.uuid1()))

	with open(os.path.abspath(os.path.dirname(__file__)) + '/../template/redirect.tmpl') as f:
		data=f.read()
		tmpl=Template(unicode(data, 'utf-8', 'ignore'))
		body=tmpl.substitute({'url':'index.py'})
		result = body.encode('utf-8')
		return HttpResponse(result)
