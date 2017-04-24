import logger
import json_utils
import socket
import time
import web_app_server
import config
import controller


class WebAppClientHandler:
    def __init__(self):
        pass

    def handle_msg(self, msg):
        if msg is not None:
            if type(msg) is dict:
                cmd = msg['cmd']
                res = {}
                if cmd == 'query':
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

                    return res

