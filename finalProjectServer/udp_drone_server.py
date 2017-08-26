import socket
import sys
import config
import collections
import controller
import flight
import json_utils

address = config.local_address
port = 10001


class Udp_drone_server:
    def __init__(self):
        # controller.get_instance().get_server_logger.info('udp dorne server started')
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (address, port)
        self.server_socket.bind(self.server_address)
        self.connections = {}
        print 'udp dorne server started'

    def start_server(self):
        print 'server staring'
        while True:
            # Wait for a connection
            recv_data, addr = self.server_socket.recvfrom(1024)
            print 'got new msg'
            self.parse_msg(recv_data, addr[0])

    def parse_msg(self, recv_data, addr):
        if addr not in self.connections:
            handler = flight.Flight(addr)
            self.connections[addr] = handler
        if recv_data is not dict:
            recv_data = recv_data.strip('[')
            recv_data = recv_data.strip(']')
            recv_data = json_utils.str_to_json(recv_data)
        drone = self.connections[addr]
        drone.handle_msg(recv_data)

    def remove_connection(self, addr):
        if addr in self.connections:
            controller.get_instance().get_server_logger().info('removing connection: ' + addr)
            del self.connections[addr]

