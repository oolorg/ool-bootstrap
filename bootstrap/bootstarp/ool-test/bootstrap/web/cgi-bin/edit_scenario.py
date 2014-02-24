#!/usr/bin/env python
# coding: utf-8

import os
import sys
import cgi
import cgitb; cgitb.enable()
from string import Template
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/../../scripts')
from common.scenario import Scenario
import openstack.os_lbaas as os_lbaas
import log
import urllib

_scenario = None
_scenario_name = None

def get_lbaas(scenario_param):
	ret="""<table class="sample1""><caption>LBaaS</caption><tr><th width="30%">Key</th><th width="70%">Value</th></tr>"""
#        ret="<th>LBaaS</th><th></th>"
        for key in scenario_param[os_lbaas.EXTEND_SECTION].keys():
                ret += """<tr><td>%s</td><td><input type="text" style="width:90%%" value="%s" readonly>""" % (key, scenario_param[os_lbaas.EXTEND_SECTION][key])
#                ret += """<tr><td>%s</td><td><input type="text" style="width:90%%" name="%s" value="%s">""" % (key, key, scenario_param[os_lbaas.EXTEND_SECTION][key])
#                ret += """<input type="hidden" name="%s" value="%s"></input></td></tr>""" % (os_lbaas.EXTEND_SECTION, key)
        return ret

def extend_list(form, scenario_param):
        ret=""
	if scenario_param.has_key(os_lbaas.EXTEND_SECTION):
	        ret += get_lbaas(scenario_param)
        return ret

def param_list(form, scenario_param):
        ret=""
	global _scenario
	log.debug(str(scenario_param))
	for section_key in _scenario.get_sections():
		if not scenario_param.has_key(section_key):
			continue
		for key in scenario_param[section_key].keys():
			ret += """<tr><td>%s</td><td><input type="text" style="width:90%%" name="%s" value="%s">""" % (key, key, scenario_param[section_key][key])
			ret += """<input type="hidden" name="%s" value="%s"></input></td></tr>""" % (section_key, key)
	ret += extend_list(form, scenario_param)
	return ret

def show_scenario(form):
	global _scenario
	global _scenario_name
	scenario_param = _scenario.read_scenario()
	with open(os.path.abspath(os.path.dirname(__file__)) + '/../template/edit_scenario.tmpl') as f:
        	data=f.read()
		tmpl=Template(unicode(data, 'utf-8', 'ignore'))
		body=tmpl.substitute({'scenario':param_list(form, scenario_param), 'select_scenario':_scenario_name, 'scenario_name':_scenario_name})
		result = body.encode('utf-8')
		return result

def save_scenario(form):
	global _scenario
	scenario_param = _scenario.read_scenario()
	scenarios = {}
	for section in _scenario.get_sections():
		section_map = {}
		for key in form.getlist(section):
			section_map[key] = form[key]
		if len(section_map):
			scenarios[section] = section_map
	_scenario.save_scenario(scenarios)
	return show_scenario(form)

@csrf_exempt
def start(req):
	global _scenario
	global _scenario_name
	form = req.POST
	_scenario_name = form['scenario']
	_scenario = Scenario(os.path.abspath(os.path.dirname(__file__)) + '/../../scenario/' + _scenario_name)
	log.debug('scenario_name :' + _scenario_name)
	if not form.has_key('is_save'):
		return HttpResponse(show_scenario(form))
	else:
		return HttpResponse(save_scenario(form))


