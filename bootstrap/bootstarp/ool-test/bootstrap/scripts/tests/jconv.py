#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import commands
import json

print "---------------------------------------------"
print sys.argv[1]
print "---------------------------------------------"

tpl = open(sys.argv[1]).read()

ret = json.loads(tpl)

print ret
print "---------------------------------------------"
