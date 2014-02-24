#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import datetime
import logging

_LOG_PATH="/var/log/bootstrap/bootstrap.log"
#_LOG_PATH="bootstrap.log"

_DEBUG=False

debug_format="%s - [DEBUG] %s"
info_format="%s - [INFO] %s"
err_format="%s - [ERROR] %s"

def get_now():
	now = datetime.datetime.now()
	return now.strftime("%Y/%m/%d %H:%M:%S")

def debug(mes):
	logging.debug(mes)
#	if _DEBUG:
#		print debug_format % (get_now(), mes)

def info(mes):
	logging.info(mes)
	try:
		sys.stdout.write(mes + "\n")
		sys.stdout.flush()
	except Exception as e:
		return
#	print info_format % (get_now(), mes)

def error(mes):
	logging.error(mes)
#	print er_format % (get_now(), mes)

def warn(mes):
#	loggin.warn(mes)
	print debug_format % (get_now(), mes)

#logging.basicConfig(level=logging.DEBUG, filename=_LOG_PATH, format="%(asctime)s %(levelname)s %(filename)s %(funcName)s %(message)s")
logging.basicConfig(level=logging.DEBUG, filename=_LOG_PATH, format="%(asctime)s %(levelname)s %(message)s")

