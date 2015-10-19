import server
import config
import threading
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s\t(%(threadName)-10s) %(filename)s:%(lineno)d\t%(message)s')


def process_task(client_name, client_socket):
    try:
        while True:
            expr = client_socket.recv(config.EXPR_MAX_SIZE)
            logging.debug('Calculating expr: %s from client: %s' % (expr, client_name))
            # TODO: calculation here
            result = 'res:%s' % expr
            logging.info('Result: %s=%s' % (expr, result))
            client_socket.send('res:%s' % expr)
    finally:
        client_socket.close()


if __name__ == '__main__':
    backendServer = server.Server('localhost', config.PROC_PORT, process_task)
    bt = threading.Thread(target=backendServer.start(), name='backendServer')
    bt.start()