#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + "/../")
import db.db_manager as db_manager 
import db.db_wrapper as db_wrapper
import common.credentials
argvs = sys.argv

def select_stacks():
	sql=u"select * from stacks"
	c=db_manager.select(sql)
	print c
	for row in c:
		print row[0], row[1], row[2], row[3], row[4], row[5]

def select_scenarios():
	print "stub"

def delete_stack(scenario):
        rows=db_manager.select(u"select uuid from stacks where deleted=0 and scenario='" + scenario + "'")
        for uuid in rows:
                os.system("heat stack-delete " + uuid[0])
                db_wrapper.delete_stack(uuid[0])
def credentials_ref():
        auth_param="--os-auth-url=" + credentials._OS_AUTH_URL  +" --os-tenant-name=" + credentials._OS_TENANT_NAME + " --os-username=" + credentials._OS_USERNAME + " --os-password=" + credentials._OS_PASSWORD
	print auth_param
	os.system("heat " + auth_param +  " stack-list")

if argvs[1] == 'stacks':
	select_stacks()
elif argvs[1] == 'scenarios':
	select_scenarios()
elif argvs[1] == 'delete-heat':
	delete_stack("ping")
elif argvs[1] == 'source':
	os.system("source " + os.getcwd() + "/../settings/credentials")
elif argvs[1] == 'credentials':
	credentials_ref()
