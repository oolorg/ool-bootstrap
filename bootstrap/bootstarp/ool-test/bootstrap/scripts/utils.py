#!/usr/bin/env python
# -*- coding: utf-8 -*-

import log

def enc_maping(params):
    parameters = {}
    if params:
        for count, p in enumerate(params.split(';'), 1):
            try:
                (n, v) = p.split(('='), 1)
            except Exception as e:
                log.error( str(type(e)) + str(e.args) + e.message )
            parameters[n] = v
    log.debug("parameters : %s" % str(parameters))
    return parameters

def dec_maping(params):
	parameters = ""
	if params:
		for n, v in params.items():
			if len(parameters):
				parameters += ";"
			parameters += "%s=%s" % (n, v)
	return parameters

def write_line(path, lists):
	try:
		f = open(path, 'w')
		for data in lists:
			f.write(data)
			f.write('\n')
		f.close()
	except Exception as e:
		log.error( str(type(e)) + str(e.args) + e.message )
		return False
	return True

def get_key_lists(dic):
        lists = []
        for key, value in dic.items():
                lists.append(key)
	return lists

def get_value_lists(dic):
        lists = []
        for key, value in dic.items():
                lists.append(value)
        return lists

def info_message(mes):
	log.info("\n------------------------------------------\n"\
		+ str(mes) + "\n"\
		+ "------------------------------------------\n"\
		+ "Date : " + log.get_now() + "\n"\
		+ "------------------------------------------\n")

