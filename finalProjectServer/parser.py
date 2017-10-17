import controller
import config
import random
import time
import re

def parse_motor_table():
    print 'parsing motor table'
    motor_table = open('utils/raw_table_data/motor_table.txt', 'r')
    data = None
    for line in motor_table:
        try:
            if 'Yes' not in line:
                continue
            data = line.split('\t')
            args = (data[0], int(data[1]), float(data[4]), int(random.random() * 100))
            controller.get_instance().get_db().insert_to_table(config.motor_tbl_insert, args)
            print 'inserted'
        except:
            print 'failed to insert: ' + data[0]
        time.sleep(0.1)
    print 'done parsing motor table'


def parse_bat_table():
    print 'parsing bat table'
    motor_table = open('utils/raw_table_data/bat_table.txt', 'r')
    data = None
    for line in motor_table:
        try:
            data = line.split('\t')
            args = (data[0], data[5], float(data[2]), int(data[6]), int(data[1]), float(data[4]), int(random.random() * 100))
            controller.get_instance().get_db().insert_to_table(config.bat_tbl_insert, args)
            print 'inserted'
        except Exception,e:
            print str(e)
            print 'failed to insert: ' + data[0]
        time.sleep(0.1)
    print 'done parsing bat table'

def parse_prop_table():
    print 'parsing prop table'
    motor_table = open('utils/raw_table_data/prop_table.txt', 'r')
    data = None
    for line in motor_table:
        try:
            line = line.strip('\n')
            data = re.split('\t', line)
            for i in range (0, len(data)):
                if data[i] == '':
                    data[i] = 0
            if len(data) < 15:
                weight = 0
            else:
                weight = data[14]
            args = (data[0], data[5], data[1], weight, int(random.random() * 100))
            controller.get_instance().get_db().insert_to_table(config.prop_tbl_insert, args)
            print 'inserted'
        except Exception,e:
            print str(e)
            print data[11]
            print 'failed to insert: ' + data[0]
        time.sleep(0.1)
    print 'done parsing bat table'


def parse_drone_table(motor_id, batt_id, prop_id):
    print 'parsing drone table'
    drone_ids = controller.get_instance().get_db().get_all_drone_ids()
    for drone in drone_ids:
        try:
            args = (drone, motor_id, batt_id, prop_id)
            controller.get_instance().get_db().insert_to_table(config.drone_tbl_insert, args)
            print 'inserted'
        except Exception, e:
            print str(e)
            print 'failed to insert'
        time.sleep(0.1)
    print 'done parsing drone table'

if __name__ == '__main__':
    print 'starting to parse'
    #parse_motor_table()
    #parse_bat_table()
    # parse_prop_table()
    parse_drone_table(1557, 149, 10)
    print 'done parsing!'
