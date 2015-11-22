import threading
import time
from Queue import Queue
import config
import socket
import logging
import random

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s\t(%(threadName)-10s) %(filename)s:%(lineno)d\t%(message)s')

ready_tasks = []
q = Queue (config.Q_SIZE)

class Task:

    def __init__(self, id, client, expr):
        self.id = id
        self.client = client
        self.expr = expr
        self.result = None


class Server:

    def __init__ (self, host, port, processor):
        self.host = host
        self.port = port
        self.name = '%s:%d' % (host,port)
        self.processor = processor
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def start(self):
        self.socket.bind((self.host,self.port))
        logging.debug('Launching server %s' % self.name)
        self.socket.listen(config.MAX_CON)
        while 1:
            client_sock, client_addr = self.socket.accept()
            client_name = ':'.join(map(str, client_addr))
            logging.debug('Received connection from %s, processing...' % client_name)
            self.processor(client_sock,client_name)

    def __del__(self):
        self.socket.close()

def proces_new_task(client_sock, client_name):
    task_id = str(int(time.time()) + random.randrange(1,1000))
    try:
        expr = client_sock.recv(512)
        logging.debug('Receive expr: %s from client: %s' % (expr, client_name))
        task = Task(task_id, client_name,expr)
        logging.info('Putting task into queue: %s, size: %d' % (task, q.qsize()+1))
        q.put(task)
        logging.debug('Sending: %s to client: %s' % (task_id, client_name))
        client_sock.send(task.id)
    finally:
        client_sock.close()

def get_result (client_sock, client_name):

    try:
        task_id = client_sock.recv(512)
        logging.debug('Receive task_id: %s from client: %s' % (task_id, client_name))

        result = None
        for task in ready_tasks:
            if task_id == task.id:
                result = task.result
                ready_tasks.remove(task)
                break

        if result is not None:
            logging.info('Task result returned to client: %s' % result)
            client_sock.send(result)
        else:
            logging.info('Task %s not ready yet' % task_id)
    finally:
        client_sock.close()

def back_client (host, port):
    logging.debug('Connecting to backend to %s:%d' % (host, port))
    client_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client_sock.connect((host,port))
        logging.info('Connection with backend established')

        while 1:
            task = q.get()
            logging.debug('Starting processing task: %s with backend' % task)
            client_sock.send(task.expr)
            res = client_sock.recv(512)
            task.result = res
            ready_tasks.append(task)
            logging.info('Task complete: %s' % task)
            q.task_done()
    finally:
        client_sock.close()


if __name__ == '__main__':
    tsk_server = Server (config.HOST, config.TASK_PORT, proces_new_task)
    res_server = Server (config.HOST, config.RES_PORT, get_result)

    tsk_thread = threading.Thread (target = tsk_server.start, name = 'tskServer_thread')
    res_thread = threading.Thread (target = res_server.start, name = 'resServer_thread')
    back_thread = threading.Thread (target = back_client, name = 'backClient_thread', args = (config.HOST,config.PROC_PORT))

    tsk_thread.start()
    res_thread.start()
    back_thread.start()

    tsk_thread.join()
    res_thread.join()
    back_thread.join()






