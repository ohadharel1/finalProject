import socket
import sys
import thread
import web_app_client_handler
import logger

address = '132.74.214.89'
port = 10002
num_of_connection = 5


class WebAppServer:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (address, port)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.server_socket.bind(self.server_address)
        self.active_connections = []
        self.logger = logger.Logger()
        print 'web app server started'

    def start_server(self):
        self.server_socket.listen(1)

        while True:
            # Wait for a connection
            self.logger.log('waiting for web app connection')
            connection, client_address = self.server_socket.accept()
            handler = web_app_client_handler.WebAppClientHandler()
            self.active_connections.append(handler)
            thread.start_new_thread(handler.run, (connection, ))

    def get_active_connections(self):
        return self.active_connections
