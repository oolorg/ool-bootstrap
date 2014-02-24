#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import quantum.agent.dhcp_agent
#import neutron.agent.dhcp_agent
from string import Template
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + "/../")
argvs = sys.argv
import log
import utils
import common.scenario as scenario
import openstack.os_lbaas as lbaas
import api.neutron_client as neutron
import api.nova_client as nova

utils.info_message("test")

class Lbaas:

        _neutron_client = None
        _ini = {"protocol":"HTTP", "lb_method":"ROUND_ROBIN"}
        _subnet_id = "872b2dbd-2f99-4677-b664-26b0f45bbba4"
        _tenant_id = None
        _scid = "testtest"

        def __init__(self):
                self._neutron_client = neutron.get_client()
                
        def create_lb_pool(self):
                ret = ""
                fileds = {"pool":{
                                "name" : "pool-%s" % self._scid,
                                "protocol" : self._ini["protocol"],
                                "lb_method" : self._ini["lb_method"],
                                "subnet_id" : self._subnet_id
				}}
                try:
                        log.debug("pool fields %s" % str(fileds))
                        res = self._neutron_client.create_pool(fileds)
                        log.debug("create pool responce : %s " % str(res))
#                        ret = self.conv_lb_pool_res(res)
                except Exception as e:
                        log.error( str(type(e)) + str(e.args) + str(e.message) )
                        raise
                return ret

#lb = Lbaas()
#lb.create_lb_pool()
nova_client = nova.get_client()
def get_services(binary=None):
	global nova_client
	objs = nova_client.services.list(binary=binary)
	columns = ["binary", "host", "zone", "status", "state"]
	services = []
	for o in objs:
		service = {}
		for column in columns:
			data = getattr(o, column, '')
			if column == 'zone':
				data = data.split(',')
			if len(data):
				service[column] = data
		services.append(service)
	return services

def get_hosts():
	lists = []
	services = get_services(binary='nova-compute')
	for s in services:
		if s['status'] == 'enabled' and s['state'] == 'up':
			lists.append(s['host'])
	return lists

def get_keypairs():
	global nova_client
	lists = []
	keys = nova_client.keypairs.list()
	for k in keys:
		key = getattr(k, 'name', '')
		lists.append(key)
	return lists


def availability_zone_create():
        services = get_services(binary='nova-compute')
        for s in services:
                if s['status'] == 'enabled' and s['state'] == 'up':
                        if "z-%s" % (s['host']) not in s['zone']:
                                print ("create az-%s." % s['host'])
                                continue
                print ("az-%s exist." % s['host'])
        return True

ret = availability_zone_create()
#ret = get_hosts()
#ret = get_keypairs()
print ret
