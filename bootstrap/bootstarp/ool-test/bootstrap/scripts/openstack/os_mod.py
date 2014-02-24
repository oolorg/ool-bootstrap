#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import json
import time

import quantum.agent.dhcp_agent

import db.db_wrapper
#import db_nova
#import db_neutron
import db_heat

#from novaclient.v1_1 import client
import log
import api.nova_client as nova
import api.heat_client as heat
import api.neutron_client as neutron
import utils

nova_client = None
heat_client = None
neutron_client = None

class End(BaseException): pass

def initialize():
	global nova_client
	global heat_client
	global neutron_client
	nova_client = nova.get_client()
	heat_client = heat.get_client()
	neutron_client = neutron.get_client()
	if nova_client == None or heat_client == None or neutron_client == None:
		log.error("openstack auth failed")

def get_nova_client():
	global nova_client
	return nova_client

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

#def get_hosts():
#        sql_hosts="select host from services where disabled=0 and deleted=0 and `binary`='nova-compute'"
#	return db_nova.select(db_nova.get_sql_connection(), sql_hosts)

def get_ns_name(net_id):
	return quantum.agent.dhcp_agent.NS_PREFIX + net_id

def availability_zone_create():
	services = get_services(binary='nova-compute')
	for s in services:
		if s['status'] == 'enabled' and s['state'] == 'up':
			if "az-%s" % (s['host']) not in s['zone']:
				aggregate = nova_client.aggregates.create("ag-%s" % s['host'], "az-%s" % s['host'])
				aggregate_tmp = nova_client.aggregates.add_host(aggregate, s['host'])
                        	log.debug("create az-%s." % s['host'])
				continue
		log.debug("az-%s exist." % s['host'])
        return True

#def availability_zone_create():
#	sql_az="select count(*) from aggregate_metadata where deleted=0 and value='az-%s'"
#	for host in get_hosts():
#		ret=db_nova.select(db_nova.get_sql_connection(), sql_az % host[0])
#		if 0 < ret[0][0]:
#			log.debug("az-%s exist." % host[0])
#			continue	
#		else:
#			aggregate = nova_client.aggregates.create("ag-%s" % host[0], "az-%s" % host[0])
#			aggregate_tmp = nova_client.aggregates.add_host(aggregate, host[0])
#			log.debug("create az-%s." % host[0])
#	return True

def keypair_create(name):
#	sql_keys="select count(name) from key_pairs where deleted=0 and name='%s'" % name
#	ret=db_nova.select(db_nova.get_sql_connection(), sql_keys)
#	if 0 < ret[0][0]:
#		log.debug("%s exist." % name)
#		return True
	if name in get_keypairs():
		log.debug("%s exist." % name)
		return True
	else:
		keypair = nova_client.keypairs.create(name)
		script_path = os.path.abspath(os.path.dirname(__file__))
		key_path = script_path + "/../../keys/" + name + ".pem"
		f = open(key_path, 'w')
		f.write(keypair.private_key)
		f.close()
		os.chmod(key_path,0600)
		log.debug("add keypair - %s." % name)
		return True
	return  False

def flavor_exist(name):
	flavor_list = nova_client.flavors.list()
	for flavor in flavor_list:
		if flavor.name == name:
			return True
	return False

def get_subnet_uuid(name):
	ret = ""
	subnet_list = neutron_client.list_subnets()["subnets"]
	for subnet in subnet_list:
		if subnet["name"] == name:
			ret = subnet["id"]
	return ret

def get_netns(subnet_id):
	ret = ""
	network_list = neutron_client.list_networks()["networks"]
        for network in network_list:
		for subnet in network["subnets"]:
                	if subnet == subnet_id:
                        	ret = get_ns_name(network["id"])
	return ret

def create_heat(name, template, params):
	ret=""
	fields = {'stack_name': name,
			'timeout_mins': 60,
			'disable_rollback': True,
			'parameters': utils.enc_maping(params)
		}
	script_path = os.path.abspath(os.path.dirname(__file__))
        template_path = script_path + "/../../templates/" + template	
	if not os.path.exists(template_path):
		log.error("template file not exists")
		return ret
	tpl = open(template_path).read()
	fields['template'] = json.loads(tpl)
	try:
		resp = heat_client.stacks.create(**fields);
		log.debug("stack create resp (%s)" % str(resp))
	except Exception as e:
                log.error( str(type(e)) + str(e.args) + e.message )
		return ret
	for stack in heat_client.stacks.list():
		if stack.stack_name == name:
			ret = stack.id
	return ret

def conv_stack_id(ids):
	ret={}
	log.debug("conv_stack_id > ids : " + str(ids))
	sql = "select nova_instance from resource where stack_id='%s'"
	for stack_id in ids:
		log.debug("search :" + stack_id)
		while True:
        		tmp = db_heat.select(db_heat.get_sql_connection(), sql % stack_id)
			log.debug("conv_stack_id select : " + str(tmp))
			if tmp and len(tmp[0]) and tmp[0][0]:
				ret[stack_id] = tmp[0][0]
				break;
			time.sleep(5)
	log.debug("< conv_stack_id")
	return ret

def get_ipaddress(instance_ids, subnet_id):
	log.debug("get_ipaddress subnet_id(%s) instance_ids:" %  subnet_id)
	log.debug(instance_ids)
	ret = {}
	if not len(instance_ids):
		log.error("instance_ids convert faild.")
		return ret
	for instance_id in instance_ids:
		try:
			while True:
#			sql = "select ip.ip_address from ipallocations as ip, ports as port where ip.port_id=port.id and port.device_id='%s'"
#			tmp = db_neutron.select(db_neutron.get_sql_connection(), sql % instance_id)
#			log.debug("get_ipaddress tmp")
#			log.debug(tmp)
#			if tmp and len(tmp[0]):
#				ret[instance_id] = tmp[0][0]
#				break;
				ports = neutron_client.list_ports(device_id = instance_id)
				if ports.has_key('ports'):
					for port in ports['ports']:
						if port.has_key('fixed_ips') and len(port['fixed_ips']):
							log.debug("port.has_key('fixed_ips') : %s" % str(port['fixed_ips']))
							for ip in port['fixed_ips']:
								if ip['subnet_id'] == subnet_id:
				                                	ret[instance_id] = ip['ip_address']
									log.debug("ipaddr - Condition match")
									raise End() 
				time.sleep(5)
		except End:
			log.debug("ipaddr - %s" % str(ret[instance_id]))
	return ret

def delete_heat(stack_id):
	try:
		heat_client.stacks.delete(stack_id)
	except Exception as e:
		log.error( str(type(e)) + str(e.args) + str(e.message) )
		return False
	return True

initialize()
