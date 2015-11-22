import socket
import time

host = 'localhost'
port = 7050

c_sock = socket.socket (socket.AF_INET,socket.SOCK_STREAM)
c_sock.connect ((host,port))

try:
    while 1:
        data = c_sock.recv(5024)
        print 'The current counter value is: %s' %data
        do = raw_input ('Your action (inc/dec/quit): ')
        if do == 'inc' or do == 'dec':
            c_sock.send (do)
        elif do == 'quit':
            c_sock.send (do)
            c_sock.close()
        else:
            print 'Wrong input'
            continue
except:
    print 'Connection lost'
finally:
    c_sock.close()
    print 'The client socket closed.'
