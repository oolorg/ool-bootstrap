#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novaclient.v1_1 import client as nc
import common.credentials as cr

import log

def get_client():
	try: 
		os_client=nc.Client(cr._OS_USERNAME, cr._OS_PASSWORD, cr._OS_TENANT_NAME, cr._OS_AUTH_URL)
		return os_client
	except Exception as e:
		log.error( str(type(e)) + str(e.args) + e.message )
		return None
