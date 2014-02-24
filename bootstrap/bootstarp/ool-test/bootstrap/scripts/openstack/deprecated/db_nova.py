#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb 
import os
import log
import urlparse
import ConfigParser
from db_openstack import select
from db_openstack import get_option

CONF_PATH="/etc/nova/nova.conf"
conf = ConfigParser.SafeConfigParser()

def get_sql_connection():
	conf.read(CONF_PATH)
	ret = get_option("sql_connection", conf)
	return ret
	
#ret = select(get_sql_connection(), "select host from services where disabled=0 and deleted=0 and `binary`='nova-compute'")
#for row in ret:
#        print row
