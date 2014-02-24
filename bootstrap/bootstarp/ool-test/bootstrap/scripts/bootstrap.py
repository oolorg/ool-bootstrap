#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import subprocess 
import uuid
import traceback

import utils
import db.db_wrapper as db_wrapper
import openstack.os_mod as os_mod
import openstack.os_lbaas as os_lbaas
import common.credentials as cr
from common.scenario import Scenario

import log

EXTEND_SECTION="EXTEND"
REQUIRE_BASIC_KEY={"AUTH":["ssh_user"],"AP":["manager_template","agent_template"],"INSTANCE":["instance_type","key_name","subnet_name"]}
AGIP_PREFIX="agips-"
VIP_PREFIX="vip-"


def get_uuid():
	return "u%s" % str(uuid.uuid1())

class Bootstrap:

	scenario = None
	scenario_id = None
	subnet_id = None
	man_stack = None
	man_ip = None
	ag_stacks = []
	ag_instances_and_ip = []

	EXTEND_CHECK={'lbaas':os_lbaas}
	sn = None
	sn_ini = None
	extend_options = []
	
        script_path = os.path.abspath(os.path.dirname(__file__))

	def __init__(self, scid, scenario):
		self.scenario_id = scid
		self.scenario = scenario
		log.debug("scenario-id : %s" % self.scenario_id)
		log.debug("scenario-name : %s" % self.scenario)
		self.sn = Scenario(self.script_path + "/../scenario/" + self.scenario)
		self.sn_ini = self.sn.read_scenario()

	def build_start(self):
		utils.info_message("Build Start..")
	        db_wrapper.insert_scenario(self.scenario_id, self.scenario, 0)
		return True

	def build_complete(self):
		utils.info_message("Build Complete..")
		db_wrapper.update_scenario_status(self.scenario_id, 1)
#		sys.exit(0)

	def build_stacks_delete(self):
		if self.man_stack:
			os_mod.delete_heat(self.man_stack)
			db_wrapper.delete_stack(self.man_stack)
		
		if len(self.ag_stacks):
			for stack_id in self.ag_stacks:
				os_mod.delete_heat(stack_id)
				db_wrapper.delete_stack(stack_id)

	def build_faile(self):
		db_wrapper.update_scenario_status(self.scenario_id, -1)
	        log.error("Build Failed..")
		self.build_stacks_delete()
#	        sys.exit(-1)

	def load_scenario(self):
		try:
			scenario_param = self.sn_ini
			for section_key in self.sn.get_sections():
				if section_key != EXTEND_SECTION:
					if not scenario_param.has_key(section_key):
	                                        return False
					require_keys = REQUIRE_BASIC_KEY[section_key]
					for require_key in require_keys:
						if require_key not in scenario_param[section_key].keys():
							log.error("require_key is not in parameter (section:%s key:%s)" % section_key, require_key)
							return False
				else:
					if scenario_param.has_key(section_key):     
						for key in scenario_param[section_key].keys():
							if scenario_param[section_key][key] == 'True':
								func = getattr(self.EXTEND_CHECK[key], 'check_options')
								if not func(scenario_param):
									return False
								else:
									self.extend_options.append(key)

		except Exception as e:
			log.error( str(type(e)) + str(e.args) + str(e.message) + str(e) )
			return False
		return True

	def check_credentials(self):
		if not cr._OS_TENANT_NAME or not cr._OS_USERNAME or not cr._OS_PASSWORD or not cr._OS_AUTH_URL:
			return False
		return True

	def get_template_parameter(self, host, subnet):
		parameters = {}
		parameters['InstanceType'] = self.sn_ini['INSTANCE']['instance_type']
		parameters['KeyName'] = self.sn_ini['INSTANCE']['key_name']
		parameters['ProvHost'] = host
		parameters['SubnetId'] = subnet
		return utils.dec_maping(parameters)

	def stack_create(self):
		mn = True
		log.info("Create Stacks.")
		for host in os_mod.get_hosts():
			uid = get_uuid()
#			az = "az-%s" % host[0]
			az = "az-%s" % host
			if mn:
				muid = get_uuid()
				stack_id = os_mod.create_heat(muid, self.sn_ini['AP']['manager_template'],
						 self.get_template_parameter(az, self.subnet_id))
				if not stack_id:
					return False
#				db_wrapper.insert_stack(self.scenario_id, stack_id, "", "", "1", host[0])
				db_wrapper.insert_stack(self.scenario_id, stack_id, "", "", "1", host)
				self.man_stack = stack_id
				mn = False
			stack_id = os_mod.create_heat(uid, self.sn_ini['AP']['agent_template'],
						 self.get_template_parameter(az, self.subnet_id))
			if not stack_id:
				return False
			db_wrapper.insert_stack(self.scenario_id, stack_id, "", "", "0", host)
			self.ag_stacks.append(stack_id)
		return True

	def check_basic_option(self):
		if not os_mod.availability_zone_create():
	                log.error("availability_zone_create Error.")
	                return -1
	        if not os_mod.keypair_create(self.sn_ini['INSTANCE']['key_name']):
	                log.error("keypair_create Error.")
	                return -1
	        if not os_mod.flavor_exist(self.sn_ini['INSTANCE']['instance_type']):
	                log.error("Flavor does not exist.")
	                return -1
		return 0 

	def get_ips_path(self):
		return "%s/../tmp/%s%s" % (self.script_path, AGIP_PREFIX, str(self.scenario_id))

	def call_bootstrap(self, man_ip):
		log.debug("Call Bootstrap shell")
		try:
			ps = subprocess.check_call([self.script_path + "/bootstrap",
							self.get_ips_path(), os_mod.get_netns(self.subnet_id),
							self.sn_ini['INSTANCE']['key_name'], 
							self.sn_ini['AUTH']['ssh_user'], man_ip])
#			ps.wait(timeout=(20*60))
		except Exception as e:
			log.error( str(type(e)) + str(e.args) + e.message + str(e) )
			return False
		return True

	def output_ipaddress(self):
		log.debug("output_ipaddress >")
		ids = os_mod.conv_stack_id(self.ag_stacks)
		log.debug(ids)
		if not len(ids) or len(ids) != len(self.ag_stacks):
			return False
		iids = utils.get_value_lists(ids)
		ips = os_mod.get_ipaddress(iids, self.subnet_id)
		if not len(ips) or len(ips) != len(ids):
			return False
		self.ag_instances_and_ip = ips
		iplists = utils.get_value_lists(ips) 
		if not utils.write_line(self.get_ips_path(), iplists):
			return False
		log.debug(ips)
		netns = os_mod.get_netns(self.subnet_id)
		for sid, iid in ids.items():
			value = {'ip':ips[iid], 'netns':netns}
			db_wrapper.update_stack(sid, value)
		log.debug("< output_ipaddress")
		return True

	def get_man_ipaddress(self):
		log.debug("get_man_ipaddress >")
		if not self.man_stack:
			return None
		sid = os_mod.conv_stack_id([self.man_stack])
		if not len(sid):
			return None
		ip = os_mod.get_ipaddress([sid[self.man_stack]], self.subnet_id)
		if not len(ip):
			return None
		log.debug("< get_man_ipaddress")
		return ip[sid[self.man_stack]]

	def get_vip_path(self):
                return "%s/../tmp/%s%s" % (self.script_path, VIP_PREFIX, str(self.scenario_id))

	def extend_after_launched(self):
		if 'lbaas' in self.extend_options:
			log.info("LBaaS Build.")
			lb = os_lbaas.Create(self.scenario_id, self.sn_ini)
			ret = lb.lb_create(self.ag_instances_and_ip)
			if not ret:
				return False
			log.debug("lbaas ret : %s" % str(ret))
			if not ret['pool']:
				return False
			db_wrapper.insert_lb_scenario(ret['pool']['id'], ret['pool']['lb_method'],
						 ret['pool']['protocol'], ret['pool']['subnet_id'], self.scenario_id)
			if not ret['vip']:
				return False
			db_wrapper.insert_lb_vip(ret['vip']['id'], ret['vip']['address'], ret['pool']['id'])
			if not ret['members'] or not len(ret['members']):
				return False
			for member in ret['members']:
				db_wrapper.insert_lb_member(member['id'], member['address'],
						 member['protocol_port'], ret['pool']['id'])
			vip = [ret['vip']['address']]
			if not utils.write_line(self.get_vip_path(), vip):
                        	return False
	                log.debug("Call Bootstrap shell")
	                try:
	                        ps = subprocess.check_call([self.script_path + '/bootstrap_extend',
	                                                        self.get_vip_path(), os_mod.get_netns(self.subnet_id),
	                                                        self.sn_ini['INSTANCE']['key_name'],
	                                                        self.sn_ini['AUTH']['ssh_user'], self.man_ip, 'vip.txt'])
	                except Exception as e:
	                        log.error( str(type(e)) + str(e.args) + e.message + str(e) )
	                        return False
		return True

	def main(self):
#		self.scenario_id = str(uuid.uuid1()) Changes to the parameter.
		if not self.build_start():
			log.error("Build Start Error.")
			return -1
		if not self.check_credentials():
			log.error("Credentials failed.")
			return -1
		if not self.load_scenario():
			log.error("Scenario Configure failed.")
			return -1
		if 0 > self.check_basic_option():
			log.error("Basic Option failed.")
			return -1
		self.subnet_id = os_mod.get_subnet_uuid(self.sn_ini['INSTANCE']['subnet_name'])
		if not self.subnet_id:
			log.error("subnet id get failed.")
			return -1
		if not self.stack_create():
                	log.error("Stack Create is failed.")
                	return -1
		if not self.output_ipaddress():
			log.error("output ipaddress failed.")
			return -1
		self.man_ip = self.get_man_ipaddress()
		if not self.man_ip:
			log.error("manager ip not found.")
			return -1
                else:
                        value = {'ip':self.man_ip, 'netns':os_mod.get_netns(self.subnet_id)}
                        db_wrapper.update_stack(self.man_stack, value)
                        log.debug("manager ip is %s" % self.man_ip)
		if not self.call_bootstrap(self.man_ip):
			log.error("bootstrap shell failed.")
			return -1
                if not self.extend_after_launched():
                        log.error("Extention Build Error.")
                        return -1
		return 0

if __name__ == '__main__':
	ret = -1
	bootstrap = None
	rcpath = sys.argv[3]
	log.debug('start bootstrap - main')
	try:
		bootstrap = Bootstrap(sys.argv[1], sys.argv[2])
		ret = bootstrap.main()
	except Exception as e:
		log.error( str(type(e)) + str(e.args) + str(e.message) )
		log.error( traceback.format_exc() )
	if bootstrap:
		bootstrap.build_faile() if 0 > ret else bootstrap.build_complete()
