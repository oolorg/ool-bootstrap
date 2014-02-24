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
import openstack.os_mod as os_mod
import log

def get_vnc(stack_id, flg):
	ret = ""
	if flg == 0:
		return ret
	iids = os_mod.conv_stack_id([stack_id])
	try:
		if len (iids):
			sv = os_mod.get_nova_client().servers.get(iids[stack_id])
			url = os_mod.get_nova_client().servers.get_vnc_console(sv, 'novnc')
		if url:
			ret += """<button type="button" class="sample" onclick="window.open('%s');">VNC</button>""" % url['console']['url']
		else:
			ret += """<button type="button" class="sample" onclick="return false;" disabled>VNC</button>"""
	except Exception as e:
		log.error( str(type(e)) + str(e.args) + str(e.message) )
	return ret

def show_env(scid):
        ret=""
	rows=db_manager.select(u"select host, stack_id, ip, manager from stacks where scid='%s' and deleted=0" % scid)
        tmp=[]
        for row in rows:
                log.debug(str(row))
		ret+="""<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>""" % (row[0], row[1], row[2], 'yes' if row[3]==1 else 'no', get_vnc(row[1], row[3]))
	
	return ret

def get_netns(scid):
        rows=db_manager.select(u"select netns from stacks where scid='%s' and deleted=0 and manager=1" % scid)
	if len(rows):
		return rows[0][0]
	return '-'

def show_lbaas(scid):
	ret = ""
	ret += """<table class="sample1" style="width:60%"><caption>LBaaS</caption><tr>"""
	ret += """<th>Method</th><th>Protocol</th><th>VIP</th><th>Member IP</th>"""
	# lb_scenari x lb_vip
	rows = db_manager.select(u"select pool.method, pool.protocol, vip.vip from lb_scenario as pool, lb_vip as vip where pool.pool_id = vip.pool_id and pool.scid = '%s'" % scid)
	method = rows[0][0]
	protocol = rows[0][1]
	vip = rows[0][2]
	# lb_scenario x lb_member
	rows = db_manager.select(u"select member.ip from lb_scenario as pool, lb_member as member where pool.pool_id = member.pool_id and pool.scid = '%s'" % scid)
	members = ""
	for member in rows:
		if len(members):
			members += "<br>"
 		members += member[0]
	ret += """<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td>""" % (method, protocol, vip, members)
	ret += "</tr></table>"
	return ret

def show_extention(scid, form):
	ret = ""
	if form.has_key('lbaas') and form['lbaas'] == 'True':
		ret += show_lbaas(scid)
	return ret

def start(req):
	form = req.GET
	if not form.has_key('scid'):
		log.error('Not found Parametor scenario.')
		sys.exit(1)
	scid = form['scid']
	with open(os.path.abspath(os.path.dirname(__file__)) + '/../template/show_environment.tmpl') as f:
		data=f.read()
		tmpl=Template(unicode(data, 'utf-8', 'ignore'))
		body=tmpl.substitute({'environment':show_env(scid),'networknamespace':get_netns(scid),'extention':show_extention(scid, form)})
	return HttpResponse(body)

