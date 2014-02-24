#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from string import Template
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + "/../")
import db.db_manager as db_manager 
import db.db_wrapper as db_wrapper
argvs = sys.argv
import log


db_manager.execute(argvs[1])
