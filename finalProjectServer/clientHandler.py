import logger
import json_utils
import socket
import time


class Handler:
    def __init__(self, drone_num):
        self.connection = None
        self.msg_size = 1024
        self.drone_num = drone_num
        self.connection_closed = False
        self.logger = logger.Logger(self.drone_num)
        self.logger.log('init client handler\n')

    def send_msg(self, msg):
        if msg is not None:
            self.connection.sendall(msg)

    def rec_msg(self):
        try:
            data = self.connection.recv(self.msg_size)
            if data is not None:
                if data is None or data is '':
                    self.connection.close()
                    print 'connection closed!'
                    self.connection_closed = True
                data = str(data)
                data = data.strip('[')
                data = data.strip(']')
                print 'data after strip: ' + data
                self.logger.log('got data: ' + data)
                jsonDict = json_utils.str_to_json(data)
                print jsonDict
                if jsonDict['cmd'] == 'fin':
                    self.connection.close()
                    print 'connection closed!'
                    self.connection_closed = True


        except socket.timeout, e:
            pass
            # err = e.args[0]
            # # this next if/else is a bit redundant, but illustrates how the
            # # timeout exception is setup
            # if err == 'timed out':
            #     self.logger.log('recv timed out, retry later')
            #     return None
        # data = json_utils.json_to_str(data)
        # return data

    # def init_connection(self):
    #     self.logger.log('init connection\n')
    #     data = self.rec_msg()
    #     if data is None:
    #         return False
    #     #logger.log(data)
    #     if data['topic'] == 'init':
    #         self.msg_size = data['msg_size']
    #         self.logger.log("changed msg_size: " + str(self.msg_size))
    #     else:
    #         print data['topic']
    #     return Tru

    def main_loop(self):
        while True:
            if self.connection_closed:
                break
            self.rec_msg()
            time.sleep(0.01)


    def run(self, connection):
        self.connection = connection
        self.connection.settimeout(5)
        self.main_loop()

