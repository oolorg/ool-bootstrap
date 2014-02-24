#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import db_manager 
import log

def enc_values(params):
        parameters = ""
        if params:
                for key in params.keys():
                        if parameters != "":
                                parameters += ","
                        parameters += key + "='" + params[key] + "'"
        return parameters

def insert_stack(scid, stack_id, ip, netns, manager, host):
        sql=u"insert into stacks(scid, stack_id, ip, netns, manager, host) values ('%s', '%s', '%s', '%s', '%s', '%s')" % (scid, stack_id, ip, netns, manager, host)
	db_manager.execute(sql)

def delete_stack(sid):
	sql=u"update stacks set deleted=1 where stack_id='%s'" % sid
	db_manager.execute(sql)

def insert_scenario(uuid, scenario, status):
	sql=u"insert into scenarios(uuid, scenario, status) values ('%s', '%s', '%s')" % (uuid, scenario, status)
	db_manager.execute(sql)

def update_stack(stack_id, values):
	if not len(values):
		log.error("update stack not value.")
		return
	sql=u"update stacks set %s where stack_id='%s'" % (enc_values(values), stack_id)
	db_manager.execute(sql)

def update_scenario_status(uuid, status):
	sql=u"update scenarios set status='%s' where uuid='%s'" % (status, uuid)
	db_manager.execute(sql)

def delete_scenario(uuid):
	sql=u"delete from scenarios where uuid='%s'" % uuid
	db_manager.execute(sql)

def insert_lb_scenario(pool_id, method, protocol, subnet_id, scid):
	sql=u"insert into lb_scenario(pool_id, method, protocol, subnet_id, scid) values ('%s', '%s', '%s', '%s', '%s')" % (pool_id, method, protocol, subnet_id, scid)
	db_manager.execute(sql)

def update_lb_scenario():
	sql=u"xxx"

def delete_lb_scenario(pool_id):
	sql=u"delete from lb_scenario where pool_id='%s'" % pool_id
	db_manager.execute(sql)

def insert_lb_member(uuid, ip, port, pool_id):
        sql=u"insert into lb_member(uuid, ip, port, pool_id) values ('%s', '%s', '%s', '%s')" % (uuid, ip, port, pool_id)
        db_manager.execute(sql)

def update_lb_member():
	sql=u"xxxx"

def delete_lb_member(pool_id):
        sql=u"delete from lb_member where pool_id='%s'" % pool_id
        db_manager.execute(sql)

def insert_lb_vip(uuid, vip, pool_id):
        sql=u"insert into lb_vip(uuid, vip, pool_id) values ('%s', '%s', '%s')" % (uuid, vip, pool_id)
        db_manager.execute(sql)

def update_lb_vip():
	sql=u"xxxx"

def delete_lb_vip(pool_id):
        sql=u"delete from lb_vip where pool_id='%s'" % pool_id
        db_manager.execute(sql)
