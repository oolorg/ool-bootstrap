#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb 
import os
import log
import urlparse
import ConfigParser
from db_openstack import select
from db_openstack import get_option

CONF_PATH="/etc/heat/heat-engine.conf"
conf = ConfigParser.SafeConfigParser()

def get_sql_connection():
	conf.read(CONF_PATH)
	ret = get_option("sql_connection", conf)
	return ret

#ret = select(get_sql_connection(), "select * from resource")
#for row in ret:
#	print row

