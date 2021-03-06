import json
import os
from datetime import datetime, date, timedelta


def json_serial(obj):
    if isinstance(obj, (date, datetime, timedelta)):
        serial = str(obj)
        return serial
    raise TypeError("Type %s is not serializable"%type(obj))


def json_to_str(json_obj):
    str = json.dumps(json_obj, default=json_serial)
    return str


def str_to_json(str):
    try:
        json_obj = json.loads(str)
        return json_obj
    except Exception, e:
        print e
        return None


def str_to_file(str, file_name='json.txt', path=None):
    if path is None:
        path = os.getcwd()
    file = open(path + '/' + file_name, 'w')
    json.dump(str, file, sort_keys=True, indent=4)


def file_to_str(file_name):
    file = open(file_name, 'r')
    json_obj = json.load(file)
    return json_obj
