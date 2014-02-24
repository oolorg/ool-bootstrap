#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb 
import os
import log
import urlparse
import ConfigParser
import glob
from db_openstack import select

CONF_DIR="/etc/quantum"
conf = ConfigParser.SafeConfigParser()

#log._DEBUG=True

def get_option(option, conf):
	for section in conf.sections():
		if conf.has_option(section, option):
			return conf.get(section, option)
	if conf.default() in option:
		return conf.get("DEFAULT", option)

def get_sql_connection():
	for (root, dirs, files) in os.walk(CONF_DIR):
		for f in files:
			try:
				conf.read(os.path.join(root, f))
				ret = get_option("sql_connection", conf)
				if ret:
					return ret
			except Exception as e:
				log.debug(str(type(e)) + str(e.args) + str(e.message))

#print get_sql_connection()

#ret = select(get_sql_connection(), "select * from ipallocations")
#for row in ret:
#	print row

#print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
#ret = select("mysql://quantum:quantum@ubuntu-ct/ovs_quantum?charset=utf8", "select * from ipallocations")
#for row in ret:
#        print row	

