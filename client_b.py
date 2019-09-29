# Import socket module
import os
import time
import socket
import logging
import datetime, threading

from threading import Thread

from file_rotation_handler import SizedRotatingFileHandler

# log file names
DATA_FILE_PATH = r'C:\Users\vinusha\PycharmProjects\solidfire\datafiles'
SOURCE_DATA_FILE_PATH = DATA_FILE_PATH + '\RUvideos.csv'
DEST_DATA_FILE_PATH = DATA_FILE_PATH + '\dest_RUvideos.csv'
CLIENT_LOG = 'client_b.log'

# setting up max_bytes to 12 MB
MAX_BYTES = 12000000

# setting the chunk size to read from data file
CHUNK_SIZE = 150000

# setting the client to run for 5 minutes
RUN_TIME = 10


class Client_a():
	def __init__(self):
		# local host IP '127.0.0.1'
		self.host_ip = '127.0.0.1'
		self.logger, self.handler = self.setup_logger('CLIENT_LOG', CLIENT_LOG)
		self.logger.info('Host Ip: [{}]'.format(self.host_ip))
		# the port on which we want to connect
		self.port = 2004
		self.logger.info('connecting on Port: [{}]'.format(self.port))

	def setup_logger(self, name, log_file, level = logging.INFO):
		formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s '
									  '%(levelname)s %(message)s')


		if name == 'CLIENT_LOG':
			handler = logging.FileHandler(log_file)
		else:
			handler = SizedRotatingFileHandler(DEST_DATA_FILE_PATH,
											   maxBytes=MAX_BYTES,
											   backupCount=10,
											   interval=10)
		handler.setFormatter(formatter)

		logger = logging.getLogger(name)
		logger.setLevel(level)
		logger.addHandler(handler)

		return logger, handler

	def create_socket_connection(self):
		self.logger.info('Establishing a connection with server [{}]'.format(
			self.host_ip))
		self.socket_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# connect to server on local computer
		self.socket_conn.connect((self.host_ip, self.port))
		self.logger.info('Established a connection with server [{}]'.format(
			self.host_ip))

	def sized_rotating_filehandler(self):
		logger, handler = self.setup_logger('DATA_FILE', DEST_DATA_FILE_PATH)
		with open(SOURCE_DATA_FILE_PATH, 'rb') as f:
			for chunk in iter(lambda: f.read(CHUNK_SIZE), b''):
				if handler.shouldRollover(chunk):
					message = 'Log is going to roll over'
					self.send_data_to_server(message)
				logger.info(chunk)
				time.sleep(0.1)

	def send_data_to_server(self, message):
		# message sent to server
		self.socket_conn.send(message.encode('ascii'))
		self.socket_conn.settimeout(500.0)

		# messaga received from server
		data = self.socket_conn.recv(2048)

		# Logging the received message
		self.logger.info('Received from the server : {}'.format(
			str(data.decode('ascii'))))

	def get_cpu_memory_info(self):
		# getting the performance info
		performance_dict = {};#dict(psutil.virtual_memory()._asdict())
		# gives a single float value
		performance_dict['cpu_used'] = {};#psutil.cpu_percent()
		self.logger.info(performance_dict)
		return str(performance_dict)

	def ping_heartbeat_details(self):
		rep = os.system("ping " + self.host_ip)
		if rep == 0:
			message = 'server is up'
		else:
			message = 'server is down'
		self.send_data_to_server(message)
		threading.Timer(10, self.ping_heartbeat_details).start()

	def close_connection(self):
		# close the connection
		self.socket_conn.close()


if __name__ == '__main__':
	client = Client_a()
	client.create_socket_connection()
	message = client.get_cpu_memory_info()
	data_thread = Thread(target=client.sized_rotating_filehandler)
	data_thread.start()
	client.ping_heartbeat_details()
	thread_id = data_thread.ident
	clk_id = time.thread_time_ns()
	print(data_thread, type(data_thread), time.clock_gettime(clk_id))
	def send_perf_info():
		job_thread_1 = Thread(target=client.send_data_to_server, args=(message,))
		job_thread_1.start()
		threading.Timer(10, send_perf_info).start()




	send_perf_info()
	time_check = datetime.datetime.now()
	while True:
		time.sleep(5)
		current_time = datetime.datetime.now()
		if current_time.minute - time_check.minute > RUN_TIME:
			break
	else:
		logging.info('Client has run for the configured time, will exit now')
		client.send_data_to_server(message='exit')
