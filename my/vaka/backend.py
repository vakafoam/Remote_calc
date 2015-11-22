import server
import socket
import logging
import threading
import config

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s\t(%(threadName)-10s) %(filename)s:%(lineno)d\t%(message)s')

def process_task(client_sock, client_name):
    try:
        while 1:
            expr = client_sock.recv(512)
            logging.debug('Calculating expr: %s from client: %s' % (expr, client_name))
            res = eval (expr)
            logging.info('Result: %s=%s' % (expr, res))
            client_sock.send(str(res))
    finally:
        client_sock.close()

if __name__ == '__main__':
    back_serv = server.Server (config.HOST, config.PROC_PORT,process_task)
    back_thread = threading.Thread (target = back_serv.start(), name = 'Backend server')
    back_thread.start()