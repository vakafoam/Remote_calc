# 2015DS Sem003 Lab001
# Python example
# Dump Client Implementation
# Server Code

import sys
import socket
import os
import time

QUAD_AXE = 7777
OUT_BUF_SIZE = 10

def eat_args():
    # Eat cmd args, return filename what to dump and server where to dump
    if len(sys.argv) <= 2:
        sys.stderr.write(u'Usage: %s <file to dump> <dump server>\n' % sys.argv[0])
        sys.exit(1)
    print "Will dump  file %s to server on %s" % (sys.argv[1],sys.argv[2])
    return (sys.argv[1],sys.argv[2])

def dump_file(server_host,filename):
    # Open file for reading
    f = open(filename,'rb')
    # Connect to server
    client_socket = socket.create_connection((server_host,QUAD_AXE))
    print 'Connection established, dumping ...'

    # Dump loop
    n = 0
    data = f.read(OUT_BUF_SIZE)
    while 1:
        client_socket.send(data)
        n += len(data)
        print ' ... %d bytes sent' % n
        if len(data) < OUT_BUF_SIZE:
            break
        data = f.read(OUT_BUF_SIZE)
    f.close()
    print '... finished'
    client_socket.close()
    print 'Connection closed'


if __name__ == '__main__':
    file_to_dump,dump_server = eat_args()
    dump_file(dump_server, file_to_dump)