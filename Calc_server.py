# Server does register a client submitted task by:
#  Unique identier (generated for each task at server side)
#  Preserving originators IP (taken from client's socket)
#  Task itself (arithmetic expression)


# When a result is given for a task by a back-end the server should add this value to an existing
# task object


# Server is multi-threaded and implements thread programming patterns.

# When client connects, the server creates the thread for serving this client and delegates a
# client socket to the client thread

# Delegation thread pattern for managing connected clients:
#  When client connects, the server creates the thread for serving this client and delegates a
# client socket to the client thread
#  In client thread: the client's request is read from socket, processed (submit task or ask result):
# * If submit the task:
# · generate unique ID for a task
# · get client's IP from socket
# · read arithmetic expression given by client
# · store client's IP and task expression into tasks hash-table by taskID
# · issue notify on tasks hash table (so that all the waiting back-ends get invoked and start
# taking tasks)
# · reply client with taskID
# · wait for client to close socket
# · terminate the thread
# * If ask for result:
# · read taskID given by client
# · check if we have result for this task in the results hash-table
# reply a client with result value if there was a result else reply with no-result
# · wait for client to close socket
# · terminate the thread
#  After creating a client thread server just starts the not preserving the thread for later use.



# Producer-Consumer thread pattern for managing connected back-ends:
#  When back-end connects, the server creates thread for serving back-end, assign a back-end
# socket to a back-end thread
#  In back-end thread we do loop in:
# * If there are no tasks in tasks hash-table
# · issue wait on tasks hash table (this will stop thread until the notify is issued on tasks
# hash-table)
# * If there is task in hash-table
# · take the task from tasks hash-table (removing it from tasks hash-table)
# · get the arithmetic expression from the tasks
# · write expression into a back-end socket (so the back-end will read the expression,
# compute it and write back the value of the result)
# · read the result value from the back-end socket
# · feature the task with the result value
# · store the task into results hash-table by taskID


# Server uses only one listening socket for both Client and Back-end types of connections.