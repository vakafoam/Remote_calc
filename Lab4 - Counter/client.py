import socket
import time

host = 'localhost'
port = 5050

c_sock = socket.socket (socket.AF_INET,socket.SOCK_STREAM)
c_sock.connect ((host,port))

c_sock.send ('inc')

data = c_sock.recv(1024)
print data.decode('utf-8')





c_sock.close()
