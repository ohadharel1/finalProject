import os, time

file_name = 'logger.txt'
log_folder_path = './logs/'


class Logger:
    def __init__(self, drone_num = 0):
        self.path = None
        self.drone_num = drone_num

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
                break

    def log(self, msg):
        log_file = open(self.path, 'a')
        if msg is not None:
            print_msg = msg
        else:
            print_msg = 'got blank msg'
        log_file.write(str(time.time()) + ">> " + print_msg + '\n')
        log_file.close()

    def get_log_path(self):
        return self.path
