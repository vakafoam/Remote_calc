import time
import socket
from multiprocessing import Process, Value, Lock
from threading import Thread

host = 'localhost'
port = 7050
MAX_CON = 10


class Counter:
    def __init__ (self, initval = 50 ):
        self.val = Value('i', initval)
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

    if 0 <= counter.value() <= 100:
        counter.inc()


def func_dec (counter):

    if 0 <= counter.value() <= 100:
        counter.dec()

def handle_client (c, addr, counter):
    while 1:
        try:
            count_val = str(counter.val.value)
            c.send (count_val)
            data = c.recv(1024)
            if data == 'inc':
                func_inc(counter)
                new_value = str(counter.val.value)
                print 'Counter increased by %s. The current value is: %s' %(addr, new_value)
                c.send(new_value)
            elif data == 'dec':
                func_dec(counter)
                new_value = str(counter.val.value)
                print 'Counter decreased by %s. The current value is: %s' %(addr, new_value)
                c.send(new_value)
            elif data == 'quit':
                c.close()
                print ('The client %s left.' % (addr,))
                break
        except:
            print ('The connection with %s lost.' %(addr,))
            break

if __name__ == '__main__':

    s_sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    s_sock.bind ((host, port))
    s_sock.listen (MAX_CON)

    counter = Counter()
    procs = []

    while 1:
        c, addr = s_sock.accept()
        print 'Connection accepted with %s' % (addr,)
        t = Thread (target = handle_client, args = (c,addr,counter))
        t.start()


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


