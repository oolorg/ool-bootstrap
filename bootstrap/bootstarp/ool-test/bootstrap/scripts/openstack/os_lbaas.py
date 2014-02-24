#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import traceback

import api.neutron_client as neutron
import openstack.os_mod as os_mod
import utils
import log

EXTEND_SECTION="LBAAS"
REQUIRED_KEY=["lb_method", "protocol", "protocol_port", "subnet_name"]

def check_options(sn):
	if EXTEND_SECTION not in sn:
		return False
	for req_key in REQUIRED_KEY:
		if req_key  not in sn[EXTEND_SECTION]:
			log.error("Required lbaas the %s Not found." % req_key)
			return False
	return True

class Delete:

	neutron_client = None

	def __init__(self):
		self.neutron_client = neutron.get_client()
		if not self.neutron_client:
			raise Exception ("LBaaS", "Initialize Error.")

        def lb_pool_delete(self, pool_id):
                log.debug("lb_pool_delete : %s" % pool_id)
		self.neutron_client.delete_pool(pool_id)

        def lb_member_delete(self, member_id):
                log.debug("lb_member_delete : %s" % member_id)
		self.neutron_client.delete_member(member_id)

        def lb_vip_delete(self, vip_id):
                log.debug("lb_vip_delete : %s" % vip_id)
		self.neutron_client.delete_vip(vip_id)

        def lb_delete(self, lb_info):
                log.debug("lb_delete (%s)" % str(lb_info))	
		if lb_info.has_key('vip'):
			self.lb_vip_delete(lb_info['vip']['id'])
		if lb_info.has_key('members'):
			for member in lb_info['members']:
				self.lb_member_delete(member['id'])
		if lb_info.has_key('pool'):
			self.lb_pool_delete(lb_info['pool']['id'])


class Create:

	neutron_client = None
	ini = None
	subnet_id = None
	tenant_id = None
	scid = None

	lb_info = {}

	def __init__(self, scid, ini):
		self.ini = ini['LBAAS']
		self.scid = scid

	def initialize(self):
		if not self.neutron_client:
			self.neutron_client = neutron.get_client()
		if not self.subnet_id:
			self.subnet_id = os_mod.get_subnet_uuid(self.ini['subnet_name'])
#		if not self.tenant_id:
#			self.tenant_id = os_mod.get_tenant_id(self.ini["tenant_name"])
		if not self.neutron_client or not self.subnet_id:
			raise Exception ("LBaaS", "Initialize Error.")

	def conv_lb_pool_res(self, body):
		ret = {}
		keys = ['id', 'tenant_id', 'protocol', 'lb_method', 'subnet_id']
		for key in keys:
			if body['pool'].has_key(key):
				ret[key] = body['pool'][key]
			else:
				raise Exception ("RESPException", "pool key(%s) not found." % key)
		return ret

	def conv_lb_member_res(self, body):
		ret = {}
		keys = ['id', 'address', 'protocol_port']
		for key in keys:
			if body['member'].has_key(key):
				ret[key] = body['member'][key]
			else:
				raise Exception ("RESPException", "member key(%s) not found." % key)
		return ret

	def conv_lb_vip_res(self, body):
		ret = {}
		keys = ['id', 'address']
		for key in keys:
			if body['vip'].has_key(key):
				ret[key] = body['vip'][key]
			else:
				raise Exception ("RESPException", "vip key(%s) not found." % key)
		return ret

	def create_lb_pool(self):
		ret = ""
		fileds = {'pool':{
				'name' : "pool-%s" % self.scid,
                                'protocol' : self.ini['protocol'],
                                'lb_method' : self.ini['lb_method'],
                                'subnet_id' : self.subnet_id
				}}
		try:
			log.debug("pool fields %s" % str(fileds))
			res = self.neutron_client.create_pool(fileds)
			log.debug("create pool responce : %s " % str(res))
			ret = self.conv_lb_pool_res(res)
		except Exception as e:
			log.error( str(type(e)) + str(e.args) + str(e.message) )
			raise
		return ret

	def create_lb_member(self, pool_id, ip):
		ret = ""
		log.debug("create_lb_member (%s, %s)" % (pool_id, ip))
		fileds = {'member':{
				'address' : ip,
				'protocol_port' : self.ini['protocol_port'],
				'pool_id' : pool_id
				}}
		try:
			log.debug("member fields %s" % str(fileds))
			res = self.neutron_client.create_member(fileds)
			log.debug("create member responce : %s " % str(res))
			ret = self.conv_lb_member_res(res)
                except Exception as e:
                        log.error( str(type(e)) + str(e.args) + str(e.message) )
			raise
	        return ret

	def create_lb_vip(self, pool_id, tenant_id):
		ret = ""
		log.debug("create_lb_vip (%s) (%s)" % (pool_id, tenant_id))
                fileds = {'vip':{
				'tenant_id' : tenant_id,
                                'name' : "vip-%s" % self.scid,
                                'subnet_id' : self.subnet_id,
                                'protocol' : self.ini['protocol'],
				'protocol_port' : self.ini['protocol_port'],
				'pool_id' : pool_id
                                }}
		try:
			log.debug("vip fields %s" % str(fileds))
			res = self.neutron_client.create_vip(fileds)
			log.debug("create vip responce : %s " % str(res))
			ret = self.conv_lb_vip_res(res)
		except Exception as e:
			log.error( str(type(e)) + str(e.args) + str(e.message) )
			raise
	        return ret

	def lb_build(self, ips):
                pool_resp = self.create_lb_pool()
#                if not len(pool_resp):
#			log.error("create_lb_pool failed.")
#                        return self.lb_info
		self.lb_info['pool'] = pool_resp
		self.tenant_id = pool_resp['tenant_id']
		self.lb_info['members'] = []
                for iid, ip in ips.items():
                        member_resp = self.create_lb_member(pool_resp['id'], ip)
#                        if not len(member_resp):
#				log.error("create_member_pool failed.")
#                                return self.lb_info
			self.lb_info['members'].append(member_resp)
                vip_resp = self.create_lb_vip(pool_resp['id'], self.tenant_id)
#                if not len(vip_resp):
#			log.error("create_vip_pool failed.")
#                        return self.lb_info
		self.lb_info['vip'] = vip_resp
		return self.lb_info

	def lb_recovery(self):
		log.debug("LBaaS Recovery.")
		lb_del = Delete()
		if self.lb_info.has_key('vip'):
			log.debug("delete : vip(%s)" % self.lb_info['vip']['id'])
			lb_del.lb_vip_delete(self.lb_info['vip']['id'])
		if self.lb_info.has_key('members'):
			log.debug("delete : member(%s)" % str(self.lb_info['members']))
			for member in self.lb_info['members']:
				lb_del.lb_member_delete(member['id'])
		if self.lb_info.has_key('pool'):
			log.debug("delete : pool(%s)" % self.lb_info['pool']['id'])
			lb_del.lb_pool_delete(self.lb_info["pool"]["id"])
		return True

	def lb_create(self, ips):
		lb_info = None
		if not len(ips):
			raise Exception("ParameterException", "is not a valid lists") 
		try:
			self.initialize()
			lb_info = self.lb_build(ips)
			if not len(lb_info):
				raise Exception("BuildError", "LBaaS build error.")
		except Exception as e:
			log.error( str(type(e)) + str(e.args) + str(e.message) )
			log.error( traceback.format_exc() )
			self.lb_recovery()
			raise
		return lb_info
