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
        # self.get_flights_per_month()

    def get_table(self, table_name):
        cursor = self.db.cursor()
        cursor.execute('select * FROM ' + table_name)
        res = cursor.fetchall()
        cursor.close()
        return res

    def insert_to_table(self, tbl_statment, args):
        res = False, ''
        cursor = self.db.cursor()
        try:
            cursor.execute('REPLACE INTO ' + tbl_statment, args)
            if cursor.rowcount <= 0:
                res = False, 'No Row Was Affected'
            self.db.commit()
            res = True, ''
        except Exception, e:
            self.db.rollback()
            res = False, str(e)
        finally:
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
        cursor.close()

    def save_error_id(self, drone_num, start_time, error):
        args = (int(error), int(drone_num), start_time)
        cursor = self.db.cursor()
        cursor.execute(
            "UPDATE " + config.flight_tbl_name + " SET error_type = %s WHERE drone_num = %s AND start_flight_time = %s;", args)
        self.db.commit()
        cursor.close()

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
                result[flight_num]['comment'] = str(row['comment'])
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
                res[current_option_tag]['size'] = format(abs(max_size - random.random()), '.2f')
                res[current_option_tag]['max_payload'] = format(abs(max_payload + random.random() * 2), '.2f')
                res[current_option_tag]['time_in_air'] = abs(min_time + int(random.random() * 10))
                res[current_option_tag]['range'] = abs(min_range + int(random.random() * 20))
                res[current_option_tag]['total_price'] = abs(max_price - int(random.random() * 100))
            elif eDroneTypes[selected_drone_type] > eDroneTypes[body_type]:
                res[current_option_tag]['size'] = format(abs(max_size + random.random()), '.2f')
                res[current_option_tag]['max_payload'] = format(abs(max_payload + max(4, random.random() * 10)), '.2f')
                res[current_option_tag]['time_in_air'] = abs(min_time + max(15, int(random.random() * 30)))
                res[current_option_tag]['range'] = abs(min_range + max(25, int(random.random() * 50)))
                res[current_option_tag]['total_price'] = abs(max_price + int(random.random() * 50))
            else: #eDroneTypes[selected_drone_type] < eDroneTypes[body_type]
                res[current_option_tag]['size'] = format(abs(max_size - random.random()), '.2f')
                res[current_option_tag]['max_payload'] = format(abs(max_payload - random.random()), '.2f')
                res[current_option_tag]['time_in_air'] = abs(min_time - min(min_time - 10, int(random.random() * 10)))
                res[current_option_tag]['range'] = abs(min_range - max(min_range - 10, int(random.random() * 50)))
                res[current_option_tag]['total_price'] = abs(max_price - int(random.random() * 50))
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
            single_res_line['log_file_path'] = row['log_file_path'].replace('\\', '/')
            single_res_line['drone_num'] = row['drone_num']
            single_res_line['comment'] = row['comment']
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
            current_row_values = {}
            for key in keys_list:
                current_row_values[key] = row[key]
            complete_values_list.append(current_row_values)
        res = {'keys': keys_list,
               'values': complete_values_list}
        return res

    def update_motor_table(self, id, name, kv, weight, price):
        res = False, ''
        cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute("UPDATE %s SET name = '%s', kv = %s, weight = %s, price = %s WHERE id = %s;"%(config.motor_tbl_name, name, kv, weight, price, id))
            if cursor.rowcount <= 0:
                res = False, 'No Row Was Affected By The Statement!'
            else:
                self.db.commit()
                res = True, ''
        except Exception, e:
            res = False, str(e)
            self.db.rollback()
        finally:
            cursor.close()
            return res

    def update_table(self, args):
        res = False, ''
        cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        try:
            if args['table_name'] == config.motor_tbl_name:
                cursor.execute("UPDATE %s SET name = '%s', kv = %s, weight = %s, price = %s WHERE id = %s;"%(config.motor_tbl_name, args['name'], args['kv'], args['weight'], args['price'], args['id']))
            elif args['table_name'] == config.battery_tbl_name:
                cursor.execute("UPDATE %s SET `name`='%s', `type`='%s', `volt`=%s, `discharge_rate`=%s, `capacity`=%s, `weight`=%s, `price`=%s WHERE `id`=%s;"%(config.battery_tbl_name, args['name'], args['type'], args['volt'], args['discharge_rate'], args['capacity'], args['weight'], args['price'], args['id']))
            elif args['table_name'] == config.prop_tbl_name:
                cursor.execute("UPDATE %s SET `name`='%s', `diameter`=%s, `speed`=%s, `weight`=%s, `price`=%s WHERE `id`=%s;"%(config.prop_tbl_name, args['name'], args['diameter'], args['speed'], args['weight'], args['price'], args['id']))
            if cursor.rowcount <= 0:
                res = False, 'No Row Was Affected By The Statement!'
            else:
                self.db.commit()
                res = True, ''
        except Exception, e:
            res = False, str(e)
            self.db.rollback()
        finally:
            cursor.close()
            return res

    def add_single_to_table(self, data):
        if data['table_name'] == config.motor_tbl_name:
            args = (data['name'], data['kv'], data['weight'], data['price'])
            return self.insert_to_table(config.motor_tbl_insert, args)
        elif data['table_name'] == config.battery_tbl_name:
            args = (data['name'], data['type'], data['volt'], data['discharge_rate'], data['capacity'], data['weight'], data['price'])
            return self.insert_to_table(config.bat_tbl_insert, args)
        elif data['table_name'] == config.prop_tbl_name:
            args = (data['name'], data['diameter'], data['speed'], data['weight'], data['price'])
            return self.insert_to_table(config.prop_tbl_insert, args)

    def delete_from_table(self, data):
        res = False, ''
        cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute("DELETE FROM %s WHERE id = %s" % (data['table_name'], data['id']))
            cursor.fetchall()
            if cursor.rowcount <= 0:
                res = False, 'No Row Was Affected By The Statement!'
            else:
                self.db.commit()
                res = True, ''
        except Exception, e:
            res = False, str(e)
            self.db.rollback()
        finally:
            cursor.close()
            return res

    def add_multi_to_table(self, data):
        statement = None
        if data['table_name'] == config.motor_tbl_name:
            statement = config.motor_tbl_insert
        elif data['table_name'] == config.battery_tbl_name:
            statement = config.bat_tbl_insert
        elif data['table_name'] == config.prop_tbl_name:
            statement = config.prop_tbl_insert
        result = []
        lines = data['content'].split('\n')
        lines.pop()
        for line in lines:
            line = line.strip()
            try:
                args = line.split(',')
                if args[0] == 'name':
                    continue
                result.append(self.insert_to_table(statement, tuple(args)))
            except Exception, e:
                result.append((False, str(e)))
        return result

    def save_flight_comment(self, comment, drone_id, start_time):
        args = (comment, drone_id, start_time)
        cursor = self.db.cursor()
        cursor.execute("UPDATE " + config.flight_tbl_name + " SET comment = %s WHERE drone_num = %s AND start_flight_time = %s;", args)
        self.db.commit()

    def get_flight_comment(self, drone_id, start_time):
        args = (drone_id, start_time)
        cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT comment FROM " + config.flight_tbl_name + " WHERE drone_num = %s AND start_flight_time = %s;", args)
        query_result = cursor.fetchall()
        cursor.close()
        res = ''
        for i, row in enumerate(query_result):
            res = row['comment']
        return res

    def get_flights_per_drone(self):
        try:
            default_background_colors = ['rgba(255, 99, 132, 0.2)',
                                            'rgba(54, 162, 235, 0.2)',
                                            'rgba(255, 206, 86, 0.2)',
                                            'rgba(75, 192, 192, 0.2)',
                                            'rgba(153, 102, 255, 0.2)',
                                            'rgba(255, 159, 64, 0.2)']
            default_border_colors = ['rgba(255, 99, 132, 1)',
                                         'rgba(54, 162, 235, 1)',
                                         'rgba(255, 206, 86, 1)',
                                         'rgba(75, 192, 192, 1)',
                                         'rgba(153, 102, 255, 1)',
                                         'rgba(255, 159, 64, 1)']
            ids = []
            counters = []
            background_colors = []
            border_colors = []
            cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT drone_num FROM " + config.flight_tbl_name, )
            query_result = cursor.fetchall()
            cursor.close()
            for i, row in enumerate(query_result):
                current_id = row['drone_num']
                if current_id not in ids:
                    ids.append(current_id)
                    counters.append(1)
                    background_colors.append(default_background_colors[len(ids) % len(default_background_colors)])
                    border_colors.append(default_border_colors[len(ids) % len(default_border_colors)])
                else:
                    counters[ids.index(current_id)] += 1
            res = {'ids': ids,
                    'counters': counters,
                    'background_colors': background_colors,
                    'border_colors': border_colors}
            return res
        except Exception, e:
            print e

    def get_errors_per_drone(self):
        try:
            default_background_colors = ['rgba(255, 99, 132, 0.2)',
                                         'rgba(54, 162, 235, 0.2)',
                                         'rgba(255, 206, 86, 0.2)',
                                         'rgba(75, 192, 192, 0.2)',
                                         'rgba(153, 102, 255, 0.2)',
                                         'rgba(255, 159, 64, 0.2)']
            default_border_colors = ['rgba(255, 99, 132, 1)',
                                     'rgba(54, 162, 235, 1)',
                                     'rgba(255, 206, 86, 1)',
                                     'rgba(75, 192, 192, 1)',
                                     'rgba(153, 102, 255, 1)',
                                     'rgba(255, 159, 64, 1)']
            ids = []
            counters = []
            background_colors = []
            border_colors = []
            cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT drone_num FROM " + config.flight_tbl_name + " WHERE STATE > 2", )
            query_result = cursor.fetchall()
            cursor.close()
            for i, row in enumerate(query_result):
                current_id = row['drone_num']
                if current_id not in ids:
                    ids.append(current_id)
                    counters.append(1)
                    background_colors.append(default_background_colors[len(ids) % len(default_background_colors)])
                    border_colors.append(default_border_colors[len(ids) % len(default_border_colors)])
                else:
                    counters[ids.index(current_id)] += 1
            res = {'ids': ids,
                   'counters': counters,
                   'background_colors': background_colors,
                   'border_colors': border_colors}
            return res
        except Exception, e:
            print e

    def get_all_errors(self):
        try:
            default_background_colors = ['rgba(255, 99, 132, 0.2)',
                                         'rgba(54, 162, 235, 0.2)',
                                         'rgba(255, 206, 86, 0.2)',
                                         'rgba(75, 192, 192, 0.2)',
                                         'rgba(153, 102, 255, 0.2)',
                                         'rgba(255, 159, 64, 0.2)']
            default_border_colors = ['rgba(255, 99, 132, 1)',
                                     'rgba(54, 162, 235, 1)',
                                     'rgba(255, 206, 86, 1)',
                                     'rgba(75, 192, 192, 1)',
                                     'rgba(153, 102, 255, 1)',
                                     'rgba(255, 159, 64, 1)']
            errors = []
            counters = []
            background_colors = []
            border_colors = []
            cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT error_type FROM " + config.flight_tbl_name, )
            query_result = cursor.fetchall()
            cursor.close()
            for i, row in enumerate(query_result):
                try:
                    current_error_id = int(row['error_type'])
                    current_error = config.error_types[current_error_id]
                    if current_error not in errors:
                        errors.append(current_error)
                        counters.append(1)
                        background_colors.append(default_background_colors[len(errors) % len(default_background_colors)])
                        border_colors.append(default_border_colors[len(errors) % len(default_border_colors)])
                    else:
                        counters[errors.index(current_error)] += 1
                except:
                    pass
            res = {'errors': errors,
                   'counters': counters,
                   'background_colors': background_colors,
                   'border_colors': border_colors}
            return res
        except Exception, e:
            print e

    def get_flights_per_month(self):
        try:
            counters = [0] * 12
            cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT start_flight_time FROM " + config.flight_tbl_name, )
            query_result = cursor.fetchall()
            cursor.close()
            for i, row in enumerate(query_result):
                try:
                    # time = datetime.datetime.strptime(row['start_flight_time'], "%Y-%m-%d %H:%M:%S")
                    month = row['start_flight_time'].month - 1
                    counters[month] += 1
                except Exception, e:
                    pass
            res = {'counters': counters}
            return res
        except Exception, e:
            print e

    def get_errors_per_month(self):
        try:
            counters = [0] * 12
            cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT start_flight_time FROM " + config.flight_tbl_name + " WHERE STATE > 2", )
            query_result = cursor.fetchall()
            cursor.close()
            for i, row in enumerate(query_result):
                try:
                    # time = datetime.datetime.strptime(row['start_flight_time'], "%Y-%m-%d %H:%M:%S")
                    month = row['start_flight_time'].month - 1
                    counters[month] += 1
                except Exception, e:
                    pass
            res = {'counters': counters}
            return res
        except Exception, e:
            print e


def get_instance():
    global instance
    if instance is None:
        instance = _DB_handler()
    return instance
