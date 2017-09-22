import socket
import time
import sys
import thread
import json_utils
import config
import controller
import collections


address = '127.0.0.1'
port = 10002


class SystemServer:
    def __init__(self):
        print 'starting system server'
        self.msg_size = 405600
        self.__is_connected = False
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (address, port)
        self.__db_connected = False
        self.server_socket.connect(self.server_address)
        self.__is_connected = True
        self.__respond = None
        print 'drone server connected'

        thread.start_new_thread(self.recv_msg_thread, ())

    def is_connected(self):
        return self.__is_connected

    def is_db_connected(self):
        return self.__db_connected

    def recv_msg_thread(self):
        while self.server_socket:
            msg = self.server_socket.recv(self.msg_size)
            if msg is not None:
                self.handle_msg(json_utils.str_to_json(msg))
            time.sleep(0.1)

    def send_msg(self, msg, blocking = False):
        if type(msg) is dict :
            msg = json_utils.json_to_str(msg)
        self.server_socket.sendall(msg)
        if blocking:
            while not self.__respond:
                time.sleep(0.1)
            res = self.__respond.copy()
            self.__respond = None
            return res

    def handle_msg(self, msg):
        print 'msg recv: ' + str(msg)
        if type(msg) is dict :
            cmd = msg['cmd']
            if cmd == 'query':
                query_num = msg['query_num']
                if query_num == config.QUERY_DB_ACTIVE:
                    self.__db_connected = True
                elif query_num == config.QUERY_GET_SETUP_SUGGESTIONS:
                    controller.get_instance().set_options(msg['result'])
                    print 'options saved!'
                else:
                    if 'success' in msg:
                        msg['result']['success'] = msg['success']
                    if 'message' in msg:
                        msg['result']['message'] = msg['message']
                    if 'summery' in msg:
                        msg['result']['summery'] = msg['summery']
                    self.__respond = msg['result']

            elif cmd == 'flight':
                controller.get_instance().refresh_active_flight(msg)
