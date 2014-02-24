#!/usr/bin/env python

import subprocess
import os

if os.path.exists(os.path.abspath(os.path.dirname(__file__)) + "/../result.html"):
	os.remove(os.path.abspath(os.path.dirname(__file__)) + "/../result.html")
subprocess.Popen(["/usr/bin/python", os.path.abspath(os.path.dirname(__file__)) + "/execute.py"])
