#!/usr/bin/env python
# coding: utf-8

import cgi
import cgitb; cgitb.enable()
import sys
import urllib

def get_result(host):
        wp = urllib.urlopen(url='http://'+host+':18000/cgi-bin/verify.py')


def request(host):
	commands.getoutput('curl -s -X GET http://' + host + ':18000/cgi-bin/verify.py')

if __name__ == '__main__':
	argvs = sys.argv
	get_result(argvs[1])
