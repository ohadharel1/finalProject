import db_handler
import logger
import datetime
import time
import thread
import threading
import controller
import config

flight_status = ['ready_to_takeoff', 'airborne', 'landed']
time_check_sleep = 60*30  # 30 minutes
wait_time_after_landed = 30  # 30 seconds


class Flight:
    def __init__(self, drone_ip):
        self.drone_ip = drone_ip
        self.drone_num = self.drone_ip.split('.')[-1]
        # self.client_handler = client_handler
        self.init_time = time.time()
        self.timestamp = datetime.datetime.fromtimestamp(self.init_time).strftime("%Y-%m-%d %H:%M:%S")
        self.logger = logger.Logger(self.drone_num)
        self.state = flight_status.index('ready_to_takeoff')
        args = (int(self.drone_num), self.timestamp, self.state, self.logger.get_log_path())
        controller.get_instance().get_db().insert_to_table(config.flight_tbl_insert, args)
        self.timeout_thread = threading.Event()
        thread.start_new_thread(self.do_time_check, ())

    def change_flight_status(self, new):
        self.state = new
        self.logger.get_drone_logger().info('drone ' + str(self.drone_num) + ' status changed- ' + str(flight_status[new]))
        controller.get_instance().get_db().change_flight_status(self.drone_num, self.timestamp, self.state)
        if self.state == flight_status.index('landed'):
            self.finish_flight()

    def do_time_check(self):
        self.timeout_thread.clear()
        res = self.timeout_thread.wait(time_check_sleep)
        if not res:
            # print 'flight time is over 30 minutes. please check!'
            self.logger.get_drone_logger().info('flight time is over 30 minutes. please check!')
        if self.state != flight_status.index('landed'):
            self.change_flight_status(flight_status.index('landed'))

    def handle_msg(self, msg):
        controller.get_instance().get_server_logger().info('msg is: ' + str(msg))
        if bool(msg['is_error']):
            self.logger.get_drone_logger().critical('drone number ' + self.drone_num + ' error: ' + str(msg['cmd']))
        else:
            self.logger.get_drone_logger().info('drone number ' + self.drone_num + ' got new msg: ' + str(msg))
        if msg['drone_num'] != int(self.drone_num):
            # print 'drone num does not match!!! something is very wrong!'
            #  return
            pass
        if msg['cmd'] == 'fin':
            self.change_flight_status(flight_status.index('landed'))
            return 'fin'
        if msg['cmd'] in config.flight_status_active:
            if self.state not in config.flight_status_active:
                self.change_flight_status(flight_status.index('airborne'))
        elif msg['cmd'] in config.flight_status_before_takeoff:
            if self.state not in config.flight_status_before_takeoff:
                self.change_flight_status(flight_status.index('ready_to_takeoff'))
        elif msg['cmd'] == 'landed':
            self.change_flight_status(flight_status.index('landed'))
            self.timeout_thread.set()

        # send data to web app
        msg['drone_ip'] = self.drone_ip
        msg['is_updated'] = True
        msg['blink'] = 0
        msg['log_path'] = self.logger.get_log_path()
        msg['start_time'] = self.init_time
        controller.get_instance().refresh_active_flights(msg)

    def finish_flight(self):
        controller.get_instance().get_db().commit_flight_end_time(self.drone_num, self.timestamp)
        controller.get_instance().get_drone_server().remove_connection(self.drone_ip)
        thread.start_new_thread(self.remove_from_active_flights, ())

    def remove_from_active_flights(self):
        time.sleep(wait_time_after_landed)
        msg = {'drone_num': self.drone_num,
               'cmd': 'remove'}
        controller.get_instance().refresh_active_flights(msg)

    def get_log_file(self):
        return self.logger.get_log_path()
