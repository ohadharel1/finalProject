import drones_server
# import web_app_server
import web_server
import threading
import db_handler
import logger
import json_utils
import collections
import logging
import sys

__instance = None
__mutex = threading.Lock()


class __Controller:
    def __init__(self):
        self.__drone_server = drones_server.DronesServer()
        self.__webapp_server = web_server.WebServer()
        self.__db = db_handler.get_instance()
        self.__active_flight = {}
        self.__active_flight['status'] = {}
        self.__active_flight['cmd'] = 'flight'
        self.__server_logger = None
        self.__init_server_logger()

    def get_drone_server(self):
        return self.__drone_server

    def get_webapp_server(self):
        return self.__webapp_server

    def get_db(self):
        return self.__db

    def __init_server_logger(self):
        streamh = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        streamh.setFormatter(formatter)
        self.__server_logger = logging.getLogger("server_logger")  # server logger
        for hdlr in self.__server_logger.handlers[:]:  # remove all old handlers
            self.__server_logger.removeHandler(hdlr)
        self.__server_logger.addHandler(streamh)
        self.__server_logger.info("server logger initiated")

    def get_server_logger(self):
        return self.__server_logger

    def refresh_active_flights(self, new_flight):
        if type(new_flight) is not dict:
            return
        drone_key = 'drone_num' + str(new_flight['drone_num'])
        if new_flight['cmd'] == 'remove':
            del self.__active_flight['status'][drone_key]
            self.__webapp_server.send_broadcast_msg(json_utils.json_to_str(self.__active_flight))
            return
        if drone_key not in self.__active_flight['status']:
            self.__active_flight['status'][drone_key] = {}
        self.__active_flight['status'][drone_key] = new_flight
        self.__webapp_server.send_broadcast_msg(json_utils.json_to_str(self.__active_flight))
        self.__active_flight['status'][drone_key]['is_updated'] = False

    def get_active_flights(self):
        return self.__active_flight


def get_instance():
    global __instance, __mutex
    __mutex.acquire()
    if __instance is None:
        __instance = __Controller()
    __mutex.release()
    return __instance

