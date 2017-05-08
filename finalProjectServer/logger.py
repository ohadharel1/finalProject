import os, time, sys
import logging

file_name = 'logger.txt'
log_folder_path = './logs/'


class Logger:
    def __init__(self, drone_num = 0):
        self.path = None
        self.drone_num = drone_num
        self.drone_logger = None
        self.server_logger = None

        self.init_log_file()

    def init_log_file(self):
        cur_log_path = log_folder_path + str(self.drone_num)
        try:
            os.mkdir(cur_log_path)
        except:
            pass

        file_num = 1
        file_path = cur_log_path + "/" + str(file_num).zfill(5)
        while True:
            try:
                log_file = open(file_path, 'r')
                log_file.close()
                file_num += 1
                file_path = cur_log_path + "/" + str(file_num).zfill(5)
                continue
            except:
                self.path = file_path
                fileh = logging.FileHandler(self.path, 'a')
                streamh = logging.StreamHandler(sys.stdout)
                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                fileh.setFormatter(formatter)
                streamh.setFormatter(formatter)
                self.drone_logger = logging.getLogger("drone_logger")  # drone logger
                for hdlr in self.drone_logger.handlers[:]:  # remove all old handlers
                    self.drone_logger.removeHandler(hdlr)
                self.drone_logger.addHandler(fileh)
                self.drone_logger.addHandler(streamh)

                self.server_logger = logging.getLogger("server_logger") #server logger
                for hdlr in self.server_logger.handlers[:]:  # remove all old handlers
                    self.server_logger.removeHandler(hdlr)
                self.server_logger.addHandler(streamh)
                break

    def get_drone_logger(self):
        return self.drone_logger

    def get_server_logger(self):
        return self.server_logger

    # def log(self, msg):
    #     log_file = open(self.path, 'a')
    #     if msg is not None:
    #         print_msg = msg
    #     else:
    #         print_msg = 'got blank msg'
    #     log_file.write(str(time.time()) + ">> " + print_msg + '\n')
    #     log_file.close()

    def get_log_path(self):
        return os.path.abspath(self.path)
