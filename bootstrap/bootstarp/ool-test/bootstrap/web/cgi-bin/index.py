#!/usr/bin/env python
# coding: utf-8

import os
import sys
import cgi
import cgitb; cgitb.enable()
from string import Template
from django.http import HttpResponse
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/../../scripts')
import db.db_manager as db_manager

def scenario_status(value):
	if value < 0:
		return "Error"
	elif value == 0:
		return "Building"
	elif value == 1:
		return "Active"
	elif value == 3:
		return "Deleting"
	else:
		return "Validating"

def enc_param(params):
	parameters = ""
	if params:
		for n, v in params.items():
			if len(parameters):
				parameters += "&"
			parameters += "%s=%s" % (n, v)
	return parameters

def get_btn_verify(params):
	if params:
		return """<button type="button" class="sample" onclick="if(show_dialog('Do you validate?')){page_load('urlRequest.py?%s&mode=verify','GET',null)}">Verify</button>""" % enc_param(params)
	else:
		return """<button type="button" class="sample" onclick="return false;" disabled>Verify</button>"""

def get_btn_result(params):
	if params:
		return """<button type="button" class="sample" onclick="page_load('urlRequest.py?%s&mode=ref','GET',null)">Show Result</button>""" % enc_param(params)
	else:
		return """<button type="button" class="sample" onclick="return false" disabled>Show Result</button>"""

def get_btn_delete(params):
	if params:
		return """<button type="button" class="sample" onclick="if(show_dialog('Do you want to delete this verification environment?')){page_load('scenario_delete.py?%s','GET',null)}">Delete</button>""" % enc_param(params)
	else:
		return """<button type="button" class="sample" onclick="return false" disabled>Delete</button>"""

def get_btn_enviroment(params):
	if params:
		return """<button type="button" class="sample" onclick="page_load('show_environment.py?%s','GET',null)">Environment</button>""" % enc_param(params)
	else:
		return """<button type="button" class="sample" onclick="return false" disabled>Environment</button>"""

def get_btn_log(params):
	if params:
		return """<button type="button" class="sample" onclick="page_load('view_log.py?%s','GET',null)">Log</button>""" % enc_param(params)
	else:
		return ""


def scenario_list():
        ret=""
        rows=db_manager.select(u"select sc.uuid, sc.scenario, sc.status, lb.pool_id from scenarios as sc left outer join lb_scenario lb on sc.uuid = lb.scid")
        for row in rows:
		scid = row[0]
		parameter = {"scid":scid, "lbaas":"True" if row[3] else "False"}
		ret += """<tr><td>%s</td>""" % (row[1])
		status=scenario_status(row[2])
		ret += """<td>%s""" % (status)
		if row[2] == 1:
			ret += "</td><td>%s%s%s%s%s</td>" % (get_btn_verify(parameter), get_btn_result(parameter),
						 get_btn_delete(parameter), get_btn_enviroment(parameter), get_btn_log(parameter))
		elif row[2] < 0:
			ret += "</td><td>%s%s%s%s%s</td>" % (get_btn_verify(None), get_btn_result(None),
						 get_btn_delete(parameter), get_btn_enviroment(parameter), get_btn_log(parameter))
		else:
			ret += """<br><progress max="100"></progress></td>"""
			ret += "</td><td>%s%s%s%s%s</td>" % (get_btn_verify(None), get_btn_result(None), get_btn_delete(None), get_btn_enviroment(None), get_btn_log(parameter))
		ret += """</tr>"""
        return ret

def start(req):
	db_manager.initialize()
	with open(os.path.abspath(os.path.dirname(__file__)) + '/../template/index.tmpl') as f:
        	data=f.read()
	        tmpl=Template(unicode(data, 'utf-8', 'ignore'))
	        body=tmpl.substitute({'scenario':scenario_list()})
	        result=body.encode('utf-8')
		return HttpResponse(result)

