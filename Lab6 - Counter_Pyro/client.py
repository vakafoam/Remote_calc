import Pyro4

name = raw_input("Type your name: ")
strength = raw_input("Enter your strength (a number 1-10): ")
stren = int (strength)
daemon = Pyro4.Daemon()

try:
    ns = Pyro4.naming.locateNS()
    counter = Pyro4.Proxy ('PYRONAME:counter')
    counter.register_c (name, stren)


    while 1:
        val = counter.get_value()
        print 'The current value is: ', val
        if 0 < val < 100:
            do = raw_input("Enter your move (inc/dec): ")
            if do == 'inc':
                counter.inc(name)
            elif do == 'dec':
                counter.dec(name)
        else:
            print counter.get_result()
            break


except:
    print 'Connection lost'

