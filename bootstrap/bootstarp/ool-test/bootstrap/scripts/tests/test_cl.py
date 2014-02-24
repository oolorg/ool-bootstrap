#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from novaclient.v1_1 import client as nc 
from neutronclient.v2_0 import client as nec
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + "/../")
import api.heat_client as hc
USER="admin"
PASS="admin"
TENANT="admin"
AUTH_URL="http://localhost:5000/v2.0/"

nect = nec.Client( username=USER, password=PASS, tenant_name=TENANT, auth_url=AUTH_URL)
##param = {"fills":[{"device_id":"2027a2fb-38d3-40cf-9853-fe41facd574d"}]}
for ports in nect.list_ports(device_id = "2027a2fb-38d3-40cf-9853-fe41facd574d")["ports"]:
	print "Device : ", ports['device_id']
	print "IP : ", ports['fixed_ips']
#hct = hc.get_client()
#for stacks in hct.stacks.list():
#	print stacks

#ret = hct.stacks.get("fc2c654a-d600-4b53-b49d-eba09dd9f420")
#print ret

