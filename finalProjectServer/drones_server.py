import socket
import sys
import thread
from _socket import SOL_SOCKET, SO_REUSEADDR

import drones_client_handler
import logger

address = '10.0.0.4'
port = 10001
num_of_connection = 5


class DronesServer:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (address, port)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.server_socket.bind(self.server_address)
        self.logger = logger.Logger()
        print 'drone server started'

    def start_server(self):
        self.server_socket.listen(1)

        while True:
            # Wait for a connection
            self.logger.log('waiting for a connection')
            connection, client_address = self.server_socket.accept()
            client_ip = client_address[0]
            drone_num = client_ip.split('.')[-1]
            handler = drones_client_handler.DronesClientHandler(drone_num)
            thread.start_new_thread(handler.run, (connection, ))
