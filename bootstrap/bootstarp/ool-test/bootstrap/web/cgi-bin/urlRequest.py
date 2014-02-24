#!/usr/bin/env python
# coding: utf-8

import os
import sys
import cgi
import urllib
import cgitb; cgitb.enable()
import subprocess
import sys
from string import Template
from django.http import HttpResponse
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/../../scripts')
import db.db_manager as db_manager


def get_query(q):
        ret=""
	for k, v in q.items():
                if len(ret):
                        ret += '&'
                ret += (k + '=' + urllib.quote(v))
        return ret

def result(netns, ip):
        with open(os.path.abspath(os.path.dirname(__file__)) + '/../template/show_result.tmpl') as f:
                data=f.read()
                tmpl=Template(unicode(data, 'utf-8', 'ignore'))
                body=tmpl.substitute({'query':get_query({'netns':netns, 'ip':ip})})
                result = body.encode('utf-8')
                return result

def start(req):
	base_path = os.path.abspath(os.path.dirname(__file__))
	form=req.GET
	rows=db_manager.select(u"select ip, netns from stacks where deleted = '0' and manager = '1' and scid = '" + form['scid'] + "'")
	if form['mode'] == 'verify':
		subprocess.call(['sudo', 'ip', 'netns', 'exec',
			rows[0][1],
			'/usr/bin/python', base_path + '/scenario_verify.py' , rows[0][0]])
		f=open(base_path + '/../template/redirect.tmpl')
		data=f.read()
		tmpl=Template(unicode(data, 'utf-8', 'ignore'))
		body=tmpl.substitute({'url':'index.py'})
		return HttpResponse(body)
	else:
#		ret=subprocess.call(['sudo', 'ip', 'netns', 'exec',
#			rows[0][1],
#			'/usr/bin/python', base_path + '/cgi-bin/scenario_result.py' , rows[0][0]])
#		ret = commands.getoutput('sudo ip netns exec ' + rows[0][1] + 
#				' /usr/bin/python ' + base_path + '/scenario_result.py ' + rows[0][0])
#		f=open(base_path + '/../template/result.tmpl')
#		data=f.read()
#		tmpl=Template(unicode(data, 'utf-8', 'ignore'))
#		body=tmpl.substitute({'result':ret})
		return HttpResponse(result(rows[0][1], rows[0][0]))

