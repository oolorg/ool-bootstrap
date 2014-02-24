#!/usr/bin/env python 
# coding: utf-8

import os
import sys
import cgi
import cgitb; cgitb.enable()
from string import Template
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + "/../../scripts")
import db.db_manager as db_manager
import log

def scenario_list():
	senarios = os.listdir(os.path.abspath(os.path.dirname(__file__)) + "/../../scenario")
	rows=db_manager.select(u"select scenario from scenarios")
	ret=""
	tmp=[]
	for row in rows:
		tmp.append(row[0])
	for config in senarios:
		if len(rows) > 0:
			if config not in tmp:
				ret += """<li><span onclick="set_value('scenario','%s')"><a href="" onclick="return false;">%s</a></span></li>""" % (config, config)
		else:
			ret += """<li><span onclick="set_value('scenario','%s')"><a href="" onclick="return false;">%s</a></span></li>""" % (config, config)
	return ret

def check_scenario(form):
	if form.has_key("scenario"):
		return form['scenario']
        else:
		return ''

@csrf_exempt
def start(req):
        with open(os.path.abspath(os.path.dirname(__file__)) + '/../template/build_scenario.tmpl') as f:
		data=f.read()
		tmpl=Template(unicode(data, 'utf-8', 'ignore'))
		body=tmpl.substitute({'scenario':scenario_list(), 'select_scenario':check_scenario(req.POST)})
		result = body.encode('utf-8')
		return HttpResponse(result)

