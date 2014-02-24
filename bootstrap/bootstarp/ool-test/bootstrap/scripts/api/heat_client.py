#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from heatclient import client as hc

import common.credentials as cr
import keystone_client as kc

import log

def get_client():
        try:
		kwargs = {
			'token': kc.get_token(),
#			'insecure': args.insecure,
			'timeout': 600,
#			'ca_file': args.ca_file,
#			'cert_file': args.cert_file,
#			'key_file': args.key_file,
			'username': cr._OS_USERNAME,
			'password': cr._OS_PASSWORD
		}
		point = kc.get_endpoint("orchestration")
                os_client=hc.Client('1', endpoint=point, **kwargs)
#                os_client=hc.Client('1', endpoint=point, token=kc.get_token())
                return os_client
        except Exception as e:
                log.error( str(type(e)) + str(e.args) + e.message )
                return None

