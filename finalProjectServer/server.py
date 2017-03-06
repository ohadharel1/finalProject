import socket
import sys
import thread
import clientHandler
import logger

address = '132.74.212.168'
port = 10001
num_of_connection = 5


class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (address, port)
        self.server_socket.bind(self.server_address)
        self.logger = logger.Logger()
        self.logger.log('server started')

    def start_server(self):
        self.server_socket.listen(1)

        while True:
            # Wait for a connection
            self.logger.log('waiting for a connection')
            connection, client_address = self.server_socket.accept()
            client_ip = client_address[0]
            drone_num = client_ip.split('.')[-1]
            handler = clientHandler.Handler(drone_num)
            thread.start_new_thread(handler.run, (connection, ))
