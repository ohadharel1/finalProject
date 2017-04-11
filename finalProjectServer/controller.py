import drones_server
import web_app_server
import threading
import db_handler

__instance = None
__mutex = threading.Lock()


class __Controller:
    def __init__(self):
        self.__drone_server = drones_server.DronesServer()
        self.__webapp_server = web_app_server.WebAppServer()
        self.__db = db_handler.get_instance()

    def get_drone_server(self):
        return self.__drone_server

    def get_webapp_server(self):
        return self.__webapp_server

    def get_db(self):
        return self.__db

    # def get_db(self):
    #     return self.__db


def get_instance():
    global __instance, __mutex
    __mutex.acquire()
    if __instance is None:
        __instance = __Controller()
    __mutex.release()
    return __instance
