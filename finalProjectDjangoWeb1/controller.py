import socket_for_server
from threading import Lock
from django.shortcuts import redirect
import config
import sys, os
# sys.path.append('C:\\Users\\ohad\\OneDrive\\project\\forSchool\\final\\finalProjectDjangoWeb1\\webserver\\flight_monitor')
from flight_monitor.views import refresh_active_flights

__instance = None
__mutex = Lock()


class __Controller:
    def __init__(self):
        global __mutex
        __mutex = self
        self.__system_server = socket_for_server.SystemServer()
        self.__option_holder = None
        self.__active_flights = None
        self.__new_flight_msg = {'do_message': False,
                                 'is_takeoff': None,
                                 'drone_id': None}
        self.__current_page = config.CURRENT_PAGE_INDEX

    def get_system_server(self):
        return self.__system_server

    def get_options(self):
        return self.__option_holder

    def set_options(self, options):
        self.__option_holder = options

    def refresh_active_flight(self, active_flights):
        refresh_active_flights(active_flights)

    def get_flight_status(self):
        return self.__active_flights

    def get_current_page(self):
        return self.__current_page

    def set_current_page(self, current_page):
        self.__current_page = current_page

    def set_flight_msg(self, msg):
        status = msg['status']
        for key in status:
            value = status[key]
            if value['cmd'] == 'takeoff':
                self.__new_flight_msg['is_takeoff'] = True
                self.__new_flight_msg['do_message'] = True
                self.__new_flight_msg['drone_id'] = value['drone_num']
            elif value['cmd'] == 'landed':
                self.__new_flight_msg['is_takeoff'] = False
                self.__new_flight_msg['do_message'] = True
                self.__new_flight_msg['drone_id'] = value['drone_num']
            else:
                # do nothing
                pass
        print self.__new_flight_msg

    def get_flight_msg(self):
        flight_msg = self.__new_flight_msg.copy()
        self.__new_flight_msg['do_message'] = False
        return flight_msg

    def get_connection_status(self):
        connection_status = {}
        connection_status['webApp'] = 'green'
        if self.__system_server.is_connected():
            connection_status['server'] = 'green'
        else:
            connection_status['server'] = 'red'
        if self.__system_server.is_db_connected():
            connection_status['db'] = 'green'
        else:
            connection_status['db'] = 'red'
        return connection_status



def get_instance():
    global __instance, __mutex
    __mutex.acquire()
    if __instance is None:
        __instance = __Controller()
    __mutex.release()
    return __instance
