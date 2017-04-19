import controller
import config
import random
import time

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


if __name__ == '__main__':
    print 'starting to parse'
    #parse_motor_table()
    parse_bat_table()
    print 'done parsing!'
