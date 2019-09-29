import socket
import logging
from threading import Thread
logging.basicConfig(filename='server.log', filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

logging.info("Running Urban Planning")


# Multithreaded Python server : TCP Server Socket Thread Pool
class HandleClientThread(Thread):

    def __init__(self, ip, port, conn):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn
        self.logger = logging.getLogger('urbanGUI')
        self.logger.info("New server socket thread started for " + self.ip + ":" + str(self.port))

    def run(self):
        while True:
            self.conn.settimeout(500.0)
            data = self.conn.recv(2048)
            self.logger.info("Server received data: {}".format(str(data.decode('ascii'))))
            MESSAGE = 'Received Data: {} '.format(str(data.decode('ascii')))
            if MESSAGE == 'exit':
                self.logger.info('Client has closed the connection and sent exit signal')
                break
            self.conn.send(MESSAGE.encode('ascii'))  # echo

class Server(object):
    def __init__(self):
        # Multithreaded Python server : TCP Server Socket Program Stub
        self._tcp_ip = '0.0.0.0'
        self._tcp_port = 2004
        self.buffer_size = 2048
        
    def _create_socket(self):        
        self.tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcpServer.bind((self._tcp_ip, self._tcp_port))
        self.tcpServer.listen(5)

    def _handle_clients(self):
        threads = []
        while True:
            self.tcpServer.listen(4)
            logging.info("Multithreaded Python server : Waiting for connections from TCP clients...")
            (conn, (ip, port)) = self.tcpServer.accept()
            newthread = HandleClientThread(ip, port, conn)
            newthread.run()
            threads.append(newthread)
            for t in threads:
                t.join()

if __name__ == '__main__':
    try:
        s = Server()
        s._create_socket()
        s._handle_clients()
    except KeyboardInterrupt:
        exit()
