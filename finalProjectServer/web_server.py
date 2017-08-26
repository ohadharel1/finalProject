import socket
import sys
import thread
from _socket import SOL_SOCKET, SO_REUSEADDR
import config
import json_utils

import web_app_client_handler
import controller

address = config.local_address
port = 10002
num_of_connection = 5


class WebServer:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (address, port)
        self.server_socket.bind(self.server_address)
        # controller.get_instance().get_server_logger().info('web server started')
        print 'web server started'
        self.connections = {}

    def start_server(self):
        self.server_socket.listen(1)

        while True:
            # Wait for a connection
            connection, client_address = self.server_socket.accept()
            controller.get_instance().get_server_logger().info('web client connected')
            client_ip = client_address[0]
            handler = web_app_client_handler.WebAppClientHandler()
            self.connections[client_ip] = handler
            thread.start_new_thread(handler.run, (connection, ))

    def remove_connection(self, client_ip):
        if self.connections.has_key(client_ip):
            self.connections.pop(client_ip)

    def get_connection(self, client_ip):
        if self.connections.has_key(client_ip):
            return self.connections[client_ip]

    def send_broadcast_msg(self, msg):
        if self.connections is not None and len(self.connections) > 0:
            if type(msg) is dict:
                msg = json_utils.json_to_str(msg)
            for key in self.connections:
                conn = self.connections[key]
                conn.send_msg(msg)

