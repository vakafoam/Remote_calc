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