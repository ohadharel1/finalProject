import MySQLdb
import config
import time
import datetime
import flight
import random
import logging
import logger
import collections
import controller


instance = None

eDroneTypes = {"Heli" : 1, "Quad" : 2, "Hexa" : 3, "Octa" : 4}


class _DB_handler:
    def __init__(self):
        self.db = MySQLdb.connect(host = config.db_host, user = config.db_user, passwd = config.db_pass, db = config.db_name)
        self.logger = logger.Logger()
        self.update_motor_table(1230, 'bla', 5, 5, 5)

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

    def get_setup_suggestions(self, body_type, max_size, max_payload, min_time, min_range, max_price, num_of_iteration = 3):
        drone_type = ['Hexa', 'Octa', 'Quad', 'Heli']
        random.shuffle(drone_type)
        if body_type is not None:
            drone_type.append(body_type)
        res = {}
        for i in range(1, num_of_iteration + 1):
            current_res, current_option_tag = self.get_single_suggestion(i)
            res[current_option_tag] = current_res
            try:
                selected_drone_type = drone_type.pop()
            except:
                drone_type = ['Hexa', 'Octa', 'Quad', 'Heli']
                random.shuffle(drone_type)
                if body_type is not None:
                    drone_type.append(body_type)
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
        controller.get_instance().get_server_logger().info('res is: ' + str(res))
        return res

    def get_single_suggestion(self, index):
        current_option_tag = 'option ' + str(index)
        res = {}
        cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT name FROM " + config.motor_tbl_name)
        query_result = cursor.fetchall()
        row = query_result[int(random.random() * 100)]
        res['motor'] = row['name'].strip('"\'')
        cursor.execute("SELECT name FROM " + config.battery_tbl_name)
        query_result = cursor.fetchall()
        row = query_result[int(random.random() * 100)]
        res['bat'] = row['name']
        cursor.execute("SELECT name FROM " + config.prop_tbl_name)
        query_result = cursor.fetchall()
        row = query_result[int(random.random() * 90)]
        res['prop'] = row['name']
        return res, current_option_tag

    def get_all_finished_flights(self):
        res = {}
        cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM " + config.flight_tbl_name)
        query_result = cursor.fetchall()
        cursor.close()
        for i, row in enumerate(query_result):
            single_res_line = {}
            single_res_line['start_flight_time'] = row['start_flight_time']
            single_res_line['end_flight_time'] = row['end_flight_time']
            single_res_line['state'] = flight.flight_status[int(row['state'])]
            single_res_line['log_file_path'] = row['log_file_path']
            single_res_line['drone_num'] = row['drone_num']
            res[i] = single_res_line
        return res

    def get_report_for_drone(self, drone_num):
        cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM " + config.flight_tbl_name + ' WHERE drone_num=' + str(drone_num))
        query_result = cursor.fetchall()
        cursor.close()
        res = {}
        res['total_num_off_flights'] = len(query_result)
        res['all_flights'] = []
        total_duration = datetime.timedelta()
        max_time_in_air = datetime.timedelta()
        num_of_errors = 0
        for i, row in enumerate(query_result):
            duration = 'N/A'
            if row['end_flight_time'] is not None:
                duration = row['end_flight_time'] - row['start_flight_time']
                total_duration += duration
                if duration > max_time_in_air:
                    max_time_in_air = duration
            if row['state'] == flight.flight_status.index('error') or row['state'] == flight.flight_status.index('landed with error'):
                num_of_errors += 1
            current_flight_sum = {}
            current_flight_sum['start_flight_time'] = row['start_flight_time']
            current_flight_sum['end_flight_time'] = row['end_flight_time']
            current_flight_sum['duration'] = str(duration)
            current_flight_sum['state'] = flight.flight_status[int(row['state'])]
            res['all_flights'].append(current_flight_sum)
        res['total_time_in_air'] = str(total_duration)
        res['max_time_in_air'] = str(max_time_in_air)
        res['num_of_errors'] = num_of_errors
        return res

    def get_table_for_managing(self, table_name):
        cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM " + table_name)
        query_result = cursor.fetchall()
        keys_list = [i[0] for i in cursor.description]
        cursor.close()
        complete_values_list = []
        for i, row in enumerate(query_result):
            current_row_values = []
            for key in keys_list:
                current_row_values.append((key, row[key]))
            complete_values_list.append(current_row_values)
        res = {'keys': keys_list,
               'values': complete_values_list}
        return res

    def update_motor_table(self, id, name, kv, weight, price):
        cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE %s SET name=%s, kv=%s, weight=%s, price=%s WHERE id=%s"%(config.motor_tbl_name, name, kv, weight, price, id))
        query_result = cursor.fetchall()

def get_instance():
    global instance
    if instance is None:
        instance = _DB_handler()
    return instance
