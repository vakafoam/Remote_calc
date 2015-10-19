import logging
import socket
import sys
import config
import time

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s\t(%(threadName)-10s) %(filename)s:%(lineno)d\t%(message)s')

def send_expr(expr, host, port):
    logging.debug('Sending \'%s\' to %s:%d' % (expr, host, port))
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        logging.debug('Connection established')
        client_socket.send(expr)
        logging.debug('Expression sent')
        task_id = client_socket.recv(config.TASKID_MAX_SIZE)
        logging.debug('Received taskId: %s' % task_id)
    finally:
        client_socket.close()
    return task_id


def check_result(task_id, host, port):
    logging.debug('Asking for result for task: %s from: %s:%d' % (task_id, host, port))
    count = 0
    result = None
    while count < config.MAX_CLIENT_REQUESTS:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((host, port))
            logging.debug('Connection established')
            client_socket.send(task_id)
            logging.debug('Request sent')
            result = client_socket.recv(config.RES_MAX_SIZE)
            if result:
                logging.info('%s = %s' % (expr, result))
                break
        finally:
            client_socket.close()
        count += 1
        time.sleep(config.CLIENT_TIMEOUT)
    if not result:
        logging.error('No result for %s' % expr)




if __name__ == '__main__':
    expr = raw_input('Expression: ')
    expr_size = len(expr)
    if expr_size > config.EXPR_MAX_SIZE:
        logging.error('Expression is too long, limit: %d, but got: %d' % (config.EXPR_MAX_SIZE, expr_size))
        sys.exit(1)
    task_id = send_expr(expr, config.DEF_HOST, config.TASK_PORT)
    check_result(task_id, config.DEF_HOST, config.RES_PORT)
