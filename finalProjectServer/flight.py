import db_handler
import logger
import datetime
import time
import thread
import threading
import controller
import config
import web_app_server

flight_status = ['ready_to_takeoff', 'airborne', 'landed']
time_check_sleep = 60*30  # 30 minutes


class Flight:
    def __init__(self, drone_num, client_handler):
        self.drone_num = drone_num
        self.client_handler = client_handler
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
        self.logger.log('drone ' + str(self.drone_num) + ' status changed- ' + str(flight_status[new]))
        controller.get_instance().get_db().change_flight_status(self.drone_num, self.timestamp, self.state)
        if self.state == flight_status.index('landed'):
            self.finish_flight()

    def do_time_check(self):
        self.timeout_thread.clear()
        res = self.timeout_thread.wait(time_check_sleep)
        if not res:
            print 'flight time is over 30 minutes. please check!'
            self.logger.log('flight time is over 30 minutes. please check!')
        if self.state != flight_status.index('landed'):
            self.change_flight_status(flight_status.index('landed'))

    def handle_msg(self, msg):
        self.logger.log('drone number ' + self.drone_num + ' got new msg: ' + str(msg))
        print 'drone number ' + self.drone_num + ' got new msg: ' + str(msg)
        if msg['droneNum'] != int(self.drone_num):
            print 'drone num does not match!!! something is very wrong!'
            return
        if msg['cmd'] == 'fin':
            self.change_flight_status(flight_status.index('landed'))
            return 'fin'
        if msg['cmd'] in config.flight_status_active:
            if self.state not in config.flight_status_active:
                self.change_flight_status(flight_status.index('airborne'))
        elif msg['cmd'] in config.flight_status_before_takeoff:
            if self.state not in config.flight_status_before_takeoff:
                self.change_flight_status(flight_status.index('ready_to_takeoff'))
        elif msg['cmd'] == 'landFin':
            self.change_flight_status(flight_status.index('landed'))
            self.timeout_thread.set()

        # send data to web app
        connection = controller.get_instance().get_webapp_server()
        connection.send_msg(msg)

    def finish_flight(self):
        controller.get_instance().get_db().commit_flight_end_time(self.drone_num, self.timestamp)
        self.client_handler.close_connection()
