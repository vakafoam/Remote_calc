import logging
import socket
import config
import time

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s\t(%(threadName)-10s) %(filename)s:%(lineno)d\t%(message)s')

def send_expr (expr, host, port):
    logging.debug('Sending \'%s\' to %s:%d' % (expr, host, port))
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_sock.connect((host,port))
        logging.debug('Connection established')
        client_sock.send(expr)
        taskID = client_sock.recv(512)
        logging.debug('Received taskId: %s' % taskID)
    finally:
        client_sock.close()
    return taskID

def check_result (taskID, host, port):
    logging.debug('Asking for result for task: %s from: %s:%d' % (taskID, host, port))
    count = 0
    result = None
    while count < config.MAX_CLIENT_REQ:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_sock.connect((host,port))
            logging.debug('Connection established')
            client_sock.send (taskID)
            logging.debug('Req sent')
            result = client_sock.recv(1024)
            if result:
                logging.info('%s = %s' % (expr, result))
                break
        finally:
            client_sock.close()

        count += 1
        time.sleep(config.CLIENT_TIMEOUT)


if __name__ == '__main__':
    expr = raw_input('Enter your expression: ')
    taskID = send_expr (expr, config.HOST,config.TASK_PORT)
    check_result(taskID, config.HOST, config.RES_PORT)