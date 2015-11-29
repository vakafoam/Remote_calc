from multiprocessing import Value, Lock
import Pyro4

class Client:
    def __init__(self, name, strength):
        self.name = name
        self.strength = strength

class Counter:
    def __init__ (self, initval = 50 ):
        self.val = Value('i', initval)
        self.lock = Lock()
        self.clients = {}

    def register_c (self, name, strength):
        client = Client (name, strength)
        self.clients[name] = client.strength

    def inc(self, name):
        if 0 < self.get_value() < 100:
            with self.lock:
                self.val.value += self.clients[name]
            new_value = str(self.val.value)
            print 'Counter increased by %s. The current value is: %s' %(name, new_value)
#        else: self.get_result()

    def dec (self, name):
        if 0 < self.get_value() < 100:
            with self.lock:
                self.val.value -= self.clients[name]
            new_value = str(self.val.value)
            print 'Counter decreased by %s. The current value is: %s' %(name, new_value)
#        else: self.get_result()

    def get_value (self):
        with self.lock:
            return self.val.value

    def get_result(self):
        if self.val.value <= 0:
            r = 'Game over! The DEC team won!'
            print r
            return r
        elif self.val.value >= 100:
            r = 'Game over! The INC team won!'
            print r
            return r


if __name__ == '__main__':

    counter = Counter()

    daemon = Pyro4.Daemon()
    ns = Pyro4.naming.locateNS()
    counter_uri = daemon.register(counter)
    ns.register('counter', counter_uri)

    daemon.requestLoop()
