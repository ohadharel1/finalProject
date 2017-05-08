import MySQLdb
import config
import time
import datetime
import flight
import random
import logging


instance = None

eDroneTypes = {"Heli" : 1, "Quad" : 2, "Hexa" : 3, "Octa" : 4}


class _DB_handler:
    def __init__(self):
        self.db = MySQLdb.connect(host = config.db_host, user = config.db_user, passwd = config.db_pass, db = config.db_name)

    def get_table(self, table_name):
        cursor = self.db.cursor()
        cursor.execute('select * FROM ' + table_name)
        res = cursor.fetchall()
        cursor.close()
        return res

    def insert_to_table(self, tbl_statment, args):
        cursor = self.db.cursor()
        cursor.execute('REPLACE INTO ' + tbl_statment, args)
        res = cursor.fetchall()
        self.db.commit()
        cursor.close()
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

    def get_active_flights(self):
        try:
            cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM " + config.flight_tbl_name + " WHERE state = %s", str(flight.flight_status.index('airborne')))
            query_result = cursor.fetchall()
            result = {}
            i = 0
            for row in query_result:
                flight_num = 'flight' + str(i)
                result[flight_num] = {}
                result[flight_num]['drone_num'] = row['drone_num']
                # result[flight_num]['drone_ip'] = row['drone_ip']
                result[flight_num]['cmd'] = flight.flight_status[int(row['state'])]
                result[flight_num]['start_time'] = str(row['start_flight_time'])
                i += 1
            return result
        except Exception, e:
            return None

    def get_setup_suggestions(self, body_type, max_size, max_payload, min_time, min_range, max_price):
        drone_type = ['Hexa', 'Octa', 'Quad', 'Heli']
        random.shuffle(drone_type)
        if body_type is not None:
            drone_type.append(body_type)
        cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        res = {}
        for i in range(0, 3):
            current_option_tag = 'option_' + str(i)
            res[current_option_tag] = {}
            cursor.execute("SELECT name FROM " + config.motor_tbl_name)
            query_result = cursor.fetchall()
            row = query_result[int(random.random() * 100)]
            res[current_option_tag]['motor'] = row['name']
            cursor.execute("SELECT name FROM " + config.battery_tbl_name)
            query_result = cursor.fetchall()
            row = query_result[int(random.random() * 100)]
            res[current_option_tag]['bat'] = row['name']
            cursor.execute("SELECT name FROM " + config.prop_tbl_name)
            query_result = cursor.fetchall()
            row = query_result[int(random.random() * 90)]
            res[current_option_tag]['prop'] = row['name']
            selected_drone_type = drone_type.pop()
            res[current_option_tag]['body'] = selected_drone_type
            if eDroneTypes[selected_drone_type] == eDroneTypes[body_type]:
                res[current_option_tag]['size'] = format(max_size - random.random(), '.2f')
                res[current_option_tag]['max_payload'] = format(max_payload + random.random() * 2, '.2f')
                res[current_option_tag]['time_in_air'] = min_time + int(random.random() * 10)
                res[current_option_tag]['range'] = min_range + int(random.random() * 20)
                res[current_option_tag]['total_price'] = max_price - int(random.random() * 100)
            elif eDroneTypes[selected_drone_type] > eDroneTypes[body_type]:
                res[current_option_tag]['size'] = format(max_size + random.random(), '.2f')
                res[current_option_tag]['max_payload'] = format(max_payload + max(4, random.random() * 10), '.2f')
                res[current_option_tag]['time_in_air'] = min_time + max(15, int(random.random() * 30))
                res[current_option_tag]['range'] = min_range + max(25, int(random.random() * 50))
                res[current_option_tag]['total_price'] = max_price + int(random.random() * 50)
            else: #eDroneTypes[selected_drone_type] < eDroneTypes[body_type]
                res[current_option_tag]['size'] = format(max_size - random.random(), '.2f')
                res[current_option_tag]['max_payload'] = format(max_payload - random.random(), '.2f')
                res[current_option_tag]['time_in_air'] = min_time - min(min_time - 10, int(random.random() * 10))
                res[current_option_tag]['range'] = min_range - max(min_range - 10, int(random.random() * 50))
                res[current_option_tag]['total_price'] = max_price - int(random.random() * 50)
        return res



def get_instance():
    global instance
    if instance is None:
        instance = _DB_handler()
    return instance
