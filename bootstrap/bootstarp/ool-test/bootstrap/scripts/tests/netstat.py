#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import commands
import cgi
import cgitb; cgitb.enable()

connect = commands.getoutput("netstat -a | awk ' /ESTABLISHED/ && / *:mysql / { print $4 \" \" $6} | wc -l'")
print "Content-Type=text/html\n"
print connect
