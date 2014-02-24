#!/usr/bin/env python
# -*- coding: utf-8 -*-

from keystoneclient.v2_0 import client as kc

import os
import sys
import common.credentials as cr

import log

def get_client():
	try: 
		os_client=kc.Client(username=cr._OS_USERNAME, password=cr._OS_PASSWORD,
					 tenant_name=cr._OS_TENANT_NAME, auth_url=cr._OS_AUTH_URL)
		return os_client
	except Exception as e:
		log.error( str(type(e)) + str(e.args) + e.message )
		return None
#print kc
#print "==========================================="
#print kc.endpoints.list()
#print "==========================================="
#for user in kc.users.list():
#	print user.name
#	print user.token.id
#print "==========================================="
#print kc.services.list()

def get_token():
	return get_client().auth_token

def get_endpoint(service):
	return get_client().service_catalog.url_for(service_type=service,
                                                   endpoint_type='publicURL')

#ret=kc.tokens.authenticate(username=cr._OS_USERNAME, password=cr._OS_PASSWORD, 
#		tenant_name=cr._OS_TENANT_NAME)
#print ret

#print ret.token
#print ret.token 
