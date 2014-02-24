#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import socket

SOCK_FILENAME = '/tmp/bootstrap_unix_socket'

content = 'HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 12\r\n\r\nWelcome to Bootstrap!'

def main():
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    s.bind(SOCK_FILENAME)
    s.listen(1)
    try:
        while True:
            conn, addr = s.accept()
            print '---connected---'
            try:
                while True:
                    data = conn.recv(1024)
                    print data
                    print '-------------------------'
                    conn.send(content)
            finally:
                conn.close()
                os.remove(SOCK_FILENAME)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
