import time
import socket
from multiprocessing import Process, Value, Lock
import threading

class Counter:
    def __init__ (self, ival = 50 ):
        self.val = Value('i', ival)
        self.lock = Lock()

    def inc(self):
        with self.lock:
            self.val.value += 1

    def dec (self):
        with self.lock:
            self.val.value -= 1

    def value (self):
        with self.lock:
            return self.val.value

def func_inc (counter):

    while 0 <= counter.value() <= 100:
        counter.inc()


def func_dec (counter):

    while 0 <= counter.value() <= 100:
        counter.dec()


def handle_client (c, data, counter):
    try:
        if data == 'inc':
            func_inc(counter)
            print 'Value increased'
            c.send('The value increased, v = %d' %counter.value())
        elif data == 'dec':
            func_dec(counter)
            print 'Value decreased'
            c.send('The value decreased, v = %d' %counter.value())
    finally:
        c.close()

host = 'localhost'
port = 5050
MAX_CON = 10

s_sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
s_sock.bind ((host, port))
s_sock.listen (MAX_CON)

counter = Counter()
procs = []

while 1:
    c, addr = s_sock.accept()
    print 'Connection accepted with %s' % (addr,)
    data = c.recv(1024)

    p = Process (target = handle_client, args = (c, data, counter))
    p.start()
    print 'Process started for %s client' % (addr,)
    procs.append(p)

for p in procs: p.join()


'''
if __name__ == '__main__':

    counter = Counter()
    INCS = 2
    DECS = 5

    inc_procs = [Process (target = func_inc, args = (counter,)) for i in range (INCS)]
    dec_procs = [Process (target = func_dec, args = (counter,)) for i in range (DECS)]
    for p in inc_procs: p.start()
    for p in dec_procs: p.start()

    while 0 <= counter.value() <= 100:
        print counter.value()
        if counter.value() < 50:
            print 'DEC team leads!'
        else:
            print 'INC team leads!'
        time.sleep (1)

        if counter.value() < 10 :
            print 'Team INC is loosing... Release 1 more player!'
            p = Process (target = func_inc, args = (counter,))
            inc_procs.append(p)
            p.start()

        if counter.value() > 90:
            print 'Team DEC is loosing... Release 1 more player!'
            p = Process (target = func_dec, args = (counter,))
            dec_procs.append(p)
            p.start()


    for p in inc_procs: p.join()
    for p in dec_procs: p.join()
'''

