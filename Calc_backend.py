# Clients do connect-disconnect by request: one request - one connection and after request is served,
# client should close connection. In this task client has only 2 kinds of requests:
#  Submit computing task
#  Ask for results of a task


# Clients should NOT be notied by server when result is ready. In fact client should check if server
# has result by himself.


# Clients and Back-ends are single threaded
#
# Clients and Back-ends shall only connect to server, so there should be no listening sockets on client
# or back-end side.

import sys
import socket
import os
import time

QUAD_AXE = 7777
BUF_SIZE = 8192

def eat_args():
    # Eat cmd args, return server IP
    if len(sys.argv) <= 1:
        sys.stderr.write(u'Usage: %s <server>\n' % sys.argv[0])
        sys.exit(1)
    print "Connect to server on %s" % (sys.argv[1])
    return (sys.argv[1])

def backend_task(server_host):
    # Connect to server
    backend_socket = socket.create_connection((server_host,QUAD_AXE))
    print 'Connection established'
	# Register backend server
    data = "register....backend"
    backend_socket.send(data)
    while 1:
		# get task
        task = backend_socket.recv(BUF_SIZE)
        print "Task: " + task
		# decipher task (Warning! Use aval() function with caution!)
        result = str(eval(task))
        backend_socket.send(result)
        print "Result: " + result

def unregister ():
    # Ask the server to unregister backend & close socket
    data = 'unregister backend'
    backend_socket.send(data)
    backend_socket.close()
    print 'Connection closed'

if __name__ == '__main__':
    server_host = eat_args()
    backend_task(server_host)
    unregister ()