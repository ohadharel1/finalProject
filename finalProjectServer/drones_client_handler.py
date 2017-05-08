import logger
import json_utils
import socket
import time
import datetime
import controller
import config
import flight


class DronesClientHandler:
    def __init__(self, drone_ip):
        self.connection = None
        self.msg_size = 1024
        self.drone_ip = drone_ip
        self.drone_num = self.drone_ip.split('.')[-1]
        self.connection_closed = False
        self.flight = flight.Flight(self.drone_ip, self)

    def send_msg(self, msg):
        if msg is not None:
            self.connection.sendall(msg)

    def rec_msg(self):
        try:
            data = self.connection.recv(self.msg_size)
            if data is not None:
                if data == '':
                    return
                data = str(data)
                data = data.strip('[')
                data = data.strip(']')
                jsonDict = json_utils.str_to_json(data)
                res = self.flight.handle_msg(jsonDict)
                if res == 'fin':
                    self.close_connection()
        except socket.timeout, e:
            pass

    def main_loop(self):
        while True:
            if self.connection_closed:
                break
            self.rec_msg()
            time.sleep(0.01)
        self.connection.close()


    def run(self, connection):
        self.connection = connection
        self.connection.settimeout(5)
        self.main_loop()

    def close_connection(self):
        self.connection_closed = True
        controller.get_instance().get_drone_server().remove_connection(self.drone_ip)

    def get_flight(self):
        return self.flight


