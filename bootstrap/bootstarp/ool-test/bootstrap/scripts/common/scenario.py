#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import ConfigParser
import log

class Scenario:

        SECTIONS=["AUTH", "AP", "INSTANCE", "EXTEND"]
        EXTEND_SECTIONS=["LBAAS"]
	scenario_path = None
	conf = None
	scenario = {}

	def __init__(self, path):
		self.scenario_path = path	
		self.conf = ConfigParser.SafeConfigParser()
		self.scenario = {}

	def read_scenario(self):
		self.conf.read(self.scenario_path)
		for section in self.conf.sections():
			value = {}
			for option in self.conf.options(section):
				value[option] = self.conf.get(section, option)
			self.scenario[section] = value
		log.debug(str(self.scenario))
		return self.scenario

	def get_sections(self):
		return self.SECTIONS

	def get_extend_sections(self):
		return self.EXTEND_SECTIONS

	def get_scenario(self):
		return self.scenario

	def save_scenario(self, scenario):
		try:
			for section in scenario.keys():
				for key, value in scenario[section].items():
					log.debug("%s, %s, %s" % (section, key, value))
					self.conf.set(section, key, value)
			self.conf.write(open(self.scenario_path, 'w'))
		except Exception as e:
			log.error( str(type(e)) + str(e.args) + str(e.message))

