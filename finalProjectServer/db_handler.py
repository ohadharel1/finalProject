import MySQLdb
import config
import time
import datetime


instance = None


class _DB_handler:
    def __init__(self):
        self.db = MySQLdb.connect(host = config.db_host, user = config.db_user, passwd = config.db_pass, db = config.db_name)

    def get_table(self, table_name):
        cursor = self.db.cursor()
        cursor.execute('select * FROM ' + table_name)
        res = cursor.fetchall()
        cursor.close()
        print 'res type is: ' + str(type(res))
        print 'res is: ' + str(res)
        return res

    def insert_to_table(self, tbl_statment, args):
        cursor = self.db.cursor()
        print 'INSERT INTO ' + tbl_statment + ' ON DUPLICATE KEY UPDATE', args
        cursor.execute('REPLACE INTO ' + tbl_statment, args)
        res = cursor.fetchall()
        self.db.commit()
        cursor.close()
        print 'res type is: ' + str(type(res))
        print 'res is: ' + str(res)
        return res

    def change_flight_status(self, drone_num, timestamp, status):
        args = (status, int(drone_num), timestamp)
        cursor = self.db.cursor()
        cursor.execute("UPDATE " + config.flight_tbl_name + " SET state = %s WHERE drone_num = %s AND start_flight_time = %s;", args)
        self.db.commit()

    def commit_flight_end_time(self, drone_num, start_time):
        ts = time.time()
        end_time = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        args = (end_time, int(drone_num), start_time)
        cursor = self.db.cursor()
        cursor.execute("UPDATE " + config.flight_tbl_name + " SET end_flight_time = %s WHERE drone_num = %s AND start_flight_time = %s;", args)
        self.db.commit()

    def get_total_flight_time_for_drone(self, drone_num):
        args = (int(drone_num))
        cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT start_flight_time, end_flight_time FROM " + config.flight_tbl_name + " WHERE drone_num = %s AND state = 2", args)
        result = cursor.fetchall()
        total_time = 0
        for row in result:
            end_time = row['end_flight_time']
            start_time = row['start_flight_time']
            total_time += (end_time - start_time).total_seconds() / 60
        return total_time


def get_instance():
    global instance
    if instance is None:
        instance = _DB_handler()
    return instance
