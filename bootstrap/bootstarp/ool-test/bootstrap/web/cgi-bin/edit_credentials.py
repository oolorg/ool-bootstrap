#!/usr/bin/env python
# coding: utf-8

import os
import sys
import cgi
import cgitb; cgitb.enable()
from string import Template
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/../../scripts')
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import common.credentials as cr 
import log
def credentials_list():
        ret=""
        ret += """<tr><td>os_tenant_name</td><td><input type="text" style="width:90%%" name="os_tenant_name" value=%s></td></tr>""" % (cr._OS_TENANT_NAME)
	ret += """<tr><td>os_username</td><td><input type="text" style="width:90%%" name="os_username" value=%s></td></tr>""" % (cr._OS_USERNAME)
	ret += """<tr><td>os_password</><td><input type="text" style="width:90%%" name="os_password" value=%s></td></tr>""" % (cr._OS_PASSWORD)
	ret += """<tr><td>os_auth_url</td><td><input type="text" style="width:90%%" name="os_auth_url" value=%s></td></td></tr>""" % (cr._OS_AUTH_URL)
	return ret

def save_credentials(form):
	data = {}
        data['os_tenant_name'] = form['os_tenant_name']
        data['os_username'] = form['os_username']
        data['os_password'] = form['os_password']
        data['os_auth_url'] = form['os_auth_url']
        cr.save_config(data)

@csrf_exempt
def start(req):
	log.debug('start - edit')
	form = req.POST
	log.debug(str(form))
	log.debug(str(req))
	if form.has_key('is_save'):
		log.debug('is_save true')
		save_credentials(form)

	with open(os.path.abspath(os.path.dirname(__file__)) + '/../template/edit_credentials.tmpl') as f:
		data=f.read()
		tmpl=Template(unicode(data, 'utf-8', 'ignore'))
		body=tmpl.substitute({'credentials':credentials_list()})
		result = body.encode('utf-8')
		return HttpResponse(result)
