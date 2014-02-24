#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import socket
import os
import BaseHTTPServer,CGIHTTPServer
#from scp import SCPClient
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + "/../")
argvs = sys.argv
import log
import utils

utils.info_message("test")

#server_class = BaseHTTPServer.HTTPServer
#httpd = server_class(("169.254.169.254", 18080), CGIHTTPServer.CGIHTTPRequestHandler)
#httpd.serve_forever()

class ConnectHTTP(object):
    def __init__(self):
    	self.host = "169.254.169.253" 
    	self.port = 18080

    def connect(self):
        sock = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)

        try:
            sock.connect(self.host)
            sock.send("GET / HTTP/1.0\r\n\r\n")
            msg = ""

            while True:
                data = sock.recv(2048)
                if not data:
                    break
                msg += data

                sock.close()
                print msg 
        except Exception as e:
            print "Socket Error."
            raise

if __name__ == "__main__":
    c = ConnectHTTP()
    c.connect()
