#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from neutronclient.v2_0 import client as nec
from quantumclient.v2_0 import client as nec
import common.credentials as cr

import log

def get_client():
	try: 
		os_client=nec.Client(username=cr._OS_USERNAME, password=cr._OS_PASSWORD, tenant_name=cr._OS_TENANT_NAME, auth_url=cr._OS_AUTH_URL)
		return os_client
	except Exception as e:
		log.error( str(type(e)) + str(e.args) + e.message )
		return None
