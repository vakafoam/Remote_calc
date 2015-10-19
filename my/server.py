from Queue import Queue
import threading
import config
import logging
import socket
import time

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s\t(%(threadName)-10s) %(filename)s:%(lineno)d\t%(message)s')

queue = Queue(config.QUEUE_SIZE)
completeTasks = []


class Task:
    NEW = -1
    CONSUMED = 0
    DONE = 1

    def __init__(self, id, client, expr):
        self.id = id
        self.client = client
        self.expr = expr
        self.state = Task.NEW
        self.result = None

    def __str__(self):
        return 'id=%s; client=%s; expr=%s; state=%d; res=%s' % (
            self.id, self.client, self.expr, self.state, self.result)


class Server:
    def __init__(self, host, port, processor, max_connections=1):
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.name = '%s:%d' % (host, port)
        self.processor = processor
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        logging.debug('Launching server %s' % self.name)
        self.sock.bind((self.host, self.port))
        self.sock.listen(self.max_connections)
        logging.info('Server up and running %s' % self.name)

        while True:
            client_sock, client_addr = self.sock.accept()
            client_name = ':'.join(map(str, client_addr))
            logging.debug('Received connection from %s, processing...' % client_name)
            self.processor(client_name, client_sock)

    def __del__(self):
        if self.sock:
            self.sock.close()


def create_and_put(expr, client):
    # TODO: check queue size to avoid overflow
    task_id = '%s' % time.time()
    task = Task(task_id, client, expr)
    logging.info('Putting task into queue: %s, size: %d' % (task, queue.qsize()+1))
    queue.put(task)

    return task


def get_task_client(task_id):
    result = None
    for task in completeTasks[:]:
        if task.id == task_id and task.state == Task.DONE:
            result = task
            completeTasks.remove(task)
            break
    return result


def process_task_request(client_name, client_socket):
    try:
        expr = client_socket.recv(config.EXPR_MAX_SIZE)
        logging.debug('Receive expr: %s from client: %s' % (expr, client_name))
        task = create_and_put(expr, client_name)
        client_socket.send(task.id)
    finally:
        client_socket.close()


def process_result_request(client_name, client_socket):
    try:
        task_id = client_socket.recv(config.TASKID_MAX_SIZE)
        logging.debug('Receive task_id: %s from client: %s' % (task_id, client_name))
        task = get_task_client(task_id)
        if task is not None:
            logging.info('Task result returned to client: %s' % task)
            client_socket.send(task.result)
        else:
            logging.info('Task %s not ready yet' % task)
    finally:
        client_socket.close()


def backend_client(host, port):
    logging.debug('Connecting to backend to %s:%d' % (host, port))
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        logging.info('Connection with backend established')

        while True:
            task = queue.get()
            logging.debug('Starting processing task: %s with backend' % task)
            client_socket.send(task.expr)
            result = client_socket.recv(config.RES_MAX_SIZE)
            task.state = Task.DONE
            task.result = result
            # TODO: check overflow
            completeTasks.append(task)
            logging.info('Task complete: %s' % task)
            queue.task_done()
    finally:
        client_socket.close()


if __name__ == '__main__':
    taskServer = Server('localhost', config.TASK_PORT, process_task_request, config.MAX_CON)
    resultServer = Server('localhost', config.RES_PORT, process_result_request, config.MAX_CON)

    ts = threading.Thread(target=taskServer.start, name='taskServer')
    rs = threading.Thread(target=resultServer.start, name='resultServer')
    bc = threading.Thread(target=backend_client, name='backendClient', args=(config.DEF_HOST, config.PROC_PORT))

    ts.start()
    rs.start()
    bc.start()

    ts.join()
    rs.join()
    bc.join()
