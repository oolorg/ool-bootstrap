#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import subprocess 
import traceback

import utils
import api.heat_client as hc
import db.db_manager as db_manager
import db.db_wrapper as db_wrapper
import openstack.os_lbaas as os_lbaas

import log

class Bootstrap:

	scid = None
	extend = None

	def __init__(self, scid, extend):
		self.scid = scid
		self.extend = extend

        def release_start(self):
                utils.info_message("Release Start..")
		db_wrapper.update_scenario_status(self.scid, 3)

        def release_complete(self):
                utils.info_message("Release Complete..")
		db_wrapper.delete_scenario(self.scid)

        def release_faile(self):
                db_wrapper.update_scenario_status(self.scid, -1)
                log.error("Release Failed..")

	def stack_delete(self):
		hcl = hc.get_client()
		rows = db_manager.select(u"select stack_id from stacks where deleted=0 and scid='%s'" % self.scid)
		for stack_id in rows:
			log.debug("delete stack : %s" % str(stack_id[0]))
			try:
				hcl.stacks.delete(stack_id[0])
			except Exception as e:
				log.error( str(type(e)) + str(e.args) + str(e.message) )
			time.sleep(5)
			db_wrapper.delete_stack(stack_id[0])

	def lb_delete(self):
		lb = os_lbaas.Delete()
		lb_map = {}
		members = []
		# lb_scenari x lb_vip
		rows = db_manager.select(u"select pool.pool_id, vip.uuid from lb_scenario as pool, lb_vip as vip where pool.pool_id = vip.pool_id and pool.scid = '%s'" % self.scid)
		lb_map["pool"] = {}
		lb_map["pool"]["id"] = rows[0][0]
		lb_map["vip"] = {}
		lb_map["vip"]["id"] = rows[0][1]
		# lb_scenario x lb_member
		rows = db_manager.select(u"select member.uuid from lb_scenario as pool, lb_member as member where pool.pool_id = member.pool_id and pool.scid = '%s'" % self.scid)
		for member in rows:
			members.append({"id":member[0]})
		lb_map["members"] = members
		lb.lb_delete(lb_map)
		db_wrapper.delete_lb_scenario(lb_map["pool"]["id"])
		db_wrapper.delete_lb_vip(lb_map["pool"]["id"])
		db_wrapper.delete_lb_member(lb_map["pool"]["id"])

	def extend_release(self):
		if "lbaas" in self.extend:
			self.lb_delete()

	def delete_log(self):
		try:
			script_path = os.path.abspath(os.path.dirname(__file__))
			log_path = "%s/../logs/%s" % (script_path, self.scid)
			os.remove(log_path)
		except Exception as e:
			log.error( str(type(e)) + str(e.args) + str(e.message) )

	def main(self):
		self.stack_delete()
		self.extend_release()
		self.delete_log()
		return 0

if __name__ == '__main__':
	bootstrap = None
	ret = -1
	try:
		options = []
		argc = len(sys.argv)
		for c in range(2, argc):
			options.append(sys.argv[c])
		log.debug("option count(%d), list(%s)" % (argc, str(options)))
		bootstrap = Bootstrap(sys.argv[1], options)
		bootstrap.release_start()
		ret = bootstrap.main()
	except Exception as e:
		log.error( str(type(e)) + str(e.args) + str(e.message) )
		log.error( traceback.format_exc() )
	if bootstrap:
		bootstrap.release_faile() if 0 > ret else bootstrap.release_complete()
