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
        # self.logger = logger.Logger(self.drone_num)
        # ts = time.time()
        # timestamp = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        # args = (int(drone_num), timestamp, self.logger.get_log_path())
        # controller.get_instance().get_db().insert_to_table(config.flight_tbl_insert, args)
        print 'init client handler'

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
                print 'data after strip: ' + data
                jsonDict = json_utils.str_to_json(data)
                res = self.flight.handle_msg(jsonDict)
                print jsonDict
                if res == 'fin':
                    self.close_connection()


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

    #
    # def handle_msg(self, msg):
    #     connections = controller.get_instance().get_webapp_server().get_active_connections()
    #     if connections is None or len(connections) < 1:
    #         print 'no connections!!!'
    #     for conn in connections:
    #         conn.send_msg(msg)

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


