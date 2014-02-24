#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import commands

KEYS=['us', 'sy']
cpu = commands.getoutput("vmstat | awk 'NR==3 { print $13 \" \" $14 }' | awk '{print}'")
print "----------------------------------"
print "            CPU                   "
print "----------------------------------"
print cpu
print "----------------------------------"

info={}
for c, v in enumerate(cpu.split(' '), 0):
	info[KEYS[c]] = v
print info
print "----------------------------------"
print "\n\n\n"


#for r in zip(KEYS, ret.split(' ')):
#	print r 


connect = commands.getoutput("netstat -lat | awk ' /ESTABLISHED/ && / *:mysql / { print $4 \" \" $6}'")
print "----------------------------------"
print "            NETSTAT               "
print "----------------------------------"
print connect
print "----------------------------------"
print len(connect.split('\n'))
print "----------------------------------"
