import MySQLdb
import config




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

    def insert_to_table(self, tbl_name, args):
        cursor = self.db.cursor()
        cursor.execute('INSERT INTO ' + tbl_name + ' ON DUPLICATE KEY UPDATE', args)
        res = cursor.fetchall()
        self.db.commit()
        cursor.close()
        print 'res type is: ' + str(type(res))
        print 'res is: ' + str(res)
        return res


def get_instance():
    global instance
    if instance is None:
        instance = _DB_handler()
    return instance
