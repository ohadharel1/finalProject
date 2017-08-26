import socket
import sys
import thread
from _socket import SOL_SOCKET, SO_REUSEADDR
import config
import collections
import drones_client_handler
import controller

address = config.local_address
port = 10001
num_of_connection = 5


class DronesServer:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (address, port)
        # self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.server_socket.bind(self.server_address)
        # controller.get_server_logger().info('drone server started')
        print 'drone server started'
        self.connections = {}

    def start_server(self):
        # self.server_socket.listen(1)

        while True:
            # Wait for a connection
            connection, client_address = self.server_socket.accept()
            controller.get_instance().get_server_logger().info('drone connected')
            client_ip = client_address[0]
            handler = drones_client_handler.DronesClientHandler(client_ip)
            self.connections[client_ip] = handler
            thread.start_new_thread(handler.run, (connection, ))

    def remove_connection(self, client_ip):
        if self.connections.has_key(client_ip):
            self.connections.pop(client_ip)

    def get_connection(self, client_ip):
        if self.connections.has_key(client_ip):
            return self.connections[client_ip]
