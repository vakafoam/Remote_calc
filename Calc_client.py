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


QUAD_AXE = 7777
OUT_BUF_SIZE = 512

def eat_args():
    # User enters server host as an arg
    if len(sys.argv) <= 1:
        sys.stderr.write(u'Usage: %s <server host>\n' % sys.argv[0])
        sys.exit(1)
    print "Will connect to the server on %s" % (sys.argv[1])
    return (sys.argv[1])

def send_expr(server_host,expr):
    # Connect to server
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.create_connection((server_host,QUAD_AXE))
    print 'Connection established ...'

    # Send loop
    n = 0
    while 1:
        client_socket.send(expr)
        n += len(expr)
        print ' ... %d bytes sent' % n
        if len(expr) < OUT_BUF_SIZE:
            break
        print '... expr sent'
    taskID = client_socket.recv()
    client_socket.close()
    return taskID

def send_req (server_host, taskID):
    # Connect to server
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.create_connection((server_host,QUAD_AXE))
    # Send request
    print 'Sending taskID request...'

    # Check loop
    while 1:
        client_socket.send(taskID)
        ans = client_socket.recv()
        if ans != 0:
            print 'The result is: ' + str(ans)
            client_socket.close()
            break

if __name__ == '__main__':
    server_host = eat_args()
    expr = raw_input('Enter your expression to solve: ')
    taskID = send_expr(server_host,expr)
    send_req (server_host,taskID)
