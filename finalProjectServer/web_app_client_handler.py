import logger
import json_utils
import socket
import time
import web_app_server
import config
import controller
import os


class WebAppClientHandler:
    def __init__(self):
        pass

    def handle_msg(self, msg):
        if msg is not None:
            print 'msg is not none'
            if type(msg) is dict:
                print 'msg type is dict'
                cmd = msg['cmd']
                res = {}
                if cmd == 'query':
                    print 'cmd is query'
                    query_num = int(msg['query_num'])
                    print 'query num is ' + str(query_num)
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
                        res['result'] = result
                        res['success'] = True
                        res['query_num'] = config.QUERY_GET_CURRENT_FLIGHT_DETAILS
                    print str(res)
                    return res

