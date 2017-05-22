import time
import datetime


class Timer:
    def __init__(self, start_time = time.time()):
        self.__start_time = start_time
        self.__end_time = None

    def get_time(self):
        if self.__end_time is None:
            current_time = time.time() - self.__start_time
        else:
            current_time = self.__end_time
        return time.strftime("%H:%M:%S", time.gmtime(current_time))

    def stop_timer(self):
        self.__end_time = time.time() - self.__start_time
