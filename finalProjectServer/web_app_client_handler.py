import logger
import json_utils
import socket
import time
import config
import controller
import os
import collections


class WebAppClientHandler:
    def __init__(self):
        self.connection = None
        self.msg_size = 1024
        self.logger = controller.get_instance().get_server_logger()


    def handle_msg(self, msg):
        if msg is not None:
            if type(msg) is dict:
                cmd = msg['cmd']
                res = {}
                if cmd == 'query':
                    res['cmd'] = cmd
                    query_num = int(msg['query_num'])
                    if query_num == config.QUERY_GET_FLIGHT_TIME_FOR_DRONE:
                        drone_num = int(msg['arg1'])
                        res['result'] = controller.get_instance().get_db().get_total_flight_time_for_drone(drone_num)
                        res['success'] = True
                        res['query_num'] = config.QUERY_GET_FLIGHT_TIME_FOR_DRONE
                    if query_num == config.QUERY_GET_ACTIVE_DRONES:
                        res['result'] = controller.get_instance().get_db().get_active_flights()
                        res['success'] = True
                        res['query_num'] = config.QUERY_GET_ACTIVE_DRONES
                    if query_num == config.QUERY_GET_CURRENT_FLIGHT_DETAILS:
                        drone_ip = msg['arg1']
                        path = controller.get_instance().get_drone_server().get_connection(drone_ip).get_flight().get_log_file()
                        size = os.path.getsize(path)
                        log = open(path, 'r')
                        result = log.read(size)
                        log.close()
                        res['result'] = result
                        res['success'] = True
                        res['query_num'] = config.QUERY_GET_CURRENT_FLIGHT_DETAILS
                    if query_num == config.QUERY_GET_SETUP_SUGGESTIONS:
                        print 'got QUERY_GET_SETUP_SUGGESTIONS'
                        drone_type = msg['drone_type']
                        max_size = int(msg['max_size'])
                        max_payload = int(msg['min_payload'])
                        max_time = int(msg['min_time'])
                        max_range = int(msg['min_range'])
                        max_price = int(msg['max_price'])
                        try:
                            num_of_iterations = int(msg['iterations'])
                        except:
                            num_of_iterations = 3
                        result = controller.get_instance().get_db().get_setup_suggestions(drone_type, max_size, max_payload, max_time, max_range, max_price, num_of_iterations)
                        res['result'] = result
                        res['success'] = True
                        res['query_num'] = config.QUERY_GET_SETUP_SUGGESTIONS
                    if query_num == config.QUERY_GET_ALL_FLIGHTS:
                        self.logger.info('got QUERY_GET_ALL_FLIGHTS')
                        result = controller.get_instance().get_db().get_all_finished_flights()
                        res['result'] = result
                        res['success'] = True
                        res['query_num'] = config.QUERY_GET_ALL_FLIGHTS
                    if query_num == config.QUERY_GET_DRONE_SUM_REPORT:
                        self.logger.info('got QUERY_GET_DRONE_SUM_REPORT')
                        drone_num = int(msg['drone_num'])
                        result = controller.get_instance().get_db().get_report_for_drone(drone_num)
                        res['result'] = result
                        res['success'] = True
                        res['query_num'] = config.QUERY_GET_DRONE_SUM_REPORT
                    if query_num == config.QUERY_GET_TABLE:
                        self.logger.info('got QUERY_GET_TABLE')
                        table_name = msg['table_name']
                        result = controller.get_instance().get_db().get_table_for_managing(table_name)
                        res['result'] = result
                        res['success'] = True
                        res['query_num'] = config.QUERY_GET_TABLE
                    if query_num == config.QUERY_UPDATE_TABLE:
                        self.logger.info('got QUERY_UPDATE_TABLE')
                        table_name = msg['table_name']
                        commit_is_good = controller.get_instance().get_db().update_motor_table(msg['id'], msg['name'], msg['kv'], msg['weight'], msg['price'])
                        result = controller.get_instance().get_db().get_table_for_managing(table_name)
                        res['result'] = result
                        res['success'] = commit_is_good
                        res['query_num'] = config.QUERY_UPDATE_TABLE
                    return res

    def recv_msg_thread(self):
        while self.connection:
            msg = self.connection.recv(self.msg_size)
            if msg is not None:
                self.logger.info('got msg from web client: ' + str(msg))
                msg = json_utils.str_to_json(msg)
                res = self.handle_msg(msg)
                self.send_msg(res)
            time.sleep(0.1)

    def send_msg(self, msg):
        if self.connection is not None:
            self.logger.info('sending msg to web client: ' + str(msg))
            if type(msg) is dict:
                msg = json_utils.json_to_str(msg)
            self.connection.sendall(msg)

    def send_current_status(self):
        self.send_msg(controller.get_instance().get_active_flights())

    def send_db_status(self):
        res = {}
        res['cmd'] = 'query'
        res['query_num'] = config.QUERY_DB_ACTIVE
        table = controller.get_instance().get_db().get_table(config.battery_tbl_name)
        if table is not None:
            res['success'] = True
        else:
            res['success'] = False
        self.send_msg(res)

    def run(self, connection):
        self.connection = connection
        self.send_current_status()
        self.send_db_status()
        self.recv_msg_thread()


