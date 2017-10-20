from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

import controller
import config
import json_utils


def manage(request):
    template = loader.get_template('management/management.html')
    table = 'tblmotor'
    context = {'table': table,
               'alert_display': False,
               }
    return HttpResponse(template.render(context, request))


def get_table(request):
    template = loader.get_template('management/management_update.html')
    table = request.POST['table']
    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_GET_TABLE
    msg['table_name'] = table
    table_result = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    context = {'table': table,
               'alert': table_result['success'],
               'alert_display': False,
               'keys': table_result['keys'],
               'values': table_result['values']}
    return HttpResponse(template.render(context, request))


def table_update(request):
    template = loader.get_template('management/management_update.html')
    table_name = request.POST['table_name']
    id = request.POST['id']
    name = request.POST['name']
    kv = request.POST['kv']
    weight = request.POST['weight']
    price = request.POST['price']

    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_UPDATE_TABLE
    msg['table_name'] = table_name
    msg['id'] = id
    msg['name'] = name
    msg['kv'] = kv
    msg['weight'] = weight
    msg['price'] = price
    table_result = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    context = {'table': table_name,
               'alert': table_result['success'],
               'alert_display': True,
               'keys': table_result['keys'],
               'values': table_result['values']}
    return HttpResponse(template.render(context, request))


def get_motor_table(request):
    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_GET_TABLE
    msg['table_name'] = 'tblmotor'
    table_result = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    context = {'table': 'tblmotor',
               'result': table_result['success'],
               'alert_display': True,
               'keys': table_result['keys'],
               'values': table_result['values']}
    return HttpResponse(json_utils.json_to_str(context), content_type='application/json')


def motor_table_update(request):
    # template = loader.get_template('management/management_update.html')
    # table_name = request.POST['table_name']
    id = request.POST['motor_id']
    name = request.POST['motor_name']
    kv = request.POST['motor_kv']
    weight = request.POST['motor_weight']
    price = request.POST['motor_price']

    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_UPDATE_TABLE
    msg['table_name'] = 'tblmotor'
    msg['id'] = id
    msg['name'] = name
    msg['kv'] = kv
    msg['weight'] = weight
    msg['price'] = price
    table_result = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    context = {'table': 'tblmotor',
               'result': table_result['success'],
               'message': table_result['message'],
               'keys': table_result['keys'],
               'values': table_result['values']}
    return HttpResponse(json_utils.json_to_str(context), content_type='application/json')


def add_single_motor_table(request):
    name = request.POST['motor_name']
    kv = request.POST['motor_kv']
    weight = request.POST['motor_weight']
    price = request.POST['motor_price']

    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_ADD_SINGLE_TO_TABLE
    msg['table_name'] = 'tblmotor'
    msg['name'] = name
    msg['kv'] = kv
    msg['weight'] = weight
    msg['price'] = price
    table_result = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    context = {'table': 'tblmotor',
               'result': table_result['success'],
               'message': table_result['message'],
               'keys': table_result['keys'],
               'values': table_result['values']}
    return HttpResponse(json_utils.json_to_str(context), content_type='application/json')


def add_multi_motor_table(request):
    content = request.POST['content']

    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_ADD_MULTI_TO_TABLE
    msg['content'] = content
    msg['table_name'] = 'tblmotor'
    table_result = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    summery = ''
    for index, (result, message) in enumerate(table_result['summery']):
        if result:
            summery += 'Row number {} was added successfully\n'.format(index + 1)
        else:
            summery += 'Failed to insert row number {}: error is: {}\n'.format(index + 1, message)
    context = {'table': 'tblmotor',
               'summery': summery,
               'keys': table_result['keys'],
               'values': table_result['values']}
    return HttpResponse(json_utils.json_to_str(context), content_type='application/json')


def delete_motor_table(request):
    id = request.POST['motor_id']

    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_DELETE_FROM_TABLE
    msg['table_name'] = 'tblmotor'
    msg['id'] = id
    table_result = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    context = {'table': 'tblmotor',
                'result': table_result['success'],
               'message': table_result['message'],
               'keys': table_result['keys'],
               'values': table_result['values']}
    return HttpResponse(json_utils.json_to_str(context), content_type='application/json')

def get_bat_table(request):
    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_GET_TABLE
    msg['table_name'] = 'tblbattery'
    table_result = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    context = {'table': 'tblbattery',
               'result': table_result['success'],
               'keys': table_result['keys'],
               'values': table_result['values']}
    return HttpResponse(json_utils.json_to_str(context), content_type='application/json')


def bat_table_update(request):
    id = request.POST['bat_id']
    name = request.POST['bat_name']
    type = request.POST['bat_type']
    volt = request.POST['bat_volt']
    discharge_rate = request.POST['bat_discharge_rate']
    capacity = request.POST['bat_capacity']
    weight = request.POST['bat_weight']
    price = request.POST['bat_price']

    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_UPDATE_TABLE
    msg['table_name'] = 'tblbattery'
    msg['id'] = id
    msg['name'] = name
    msg['type'] = type
    msg['volt'] = volt
    msg['discharge_rate'] = discharge_rate
    msg['capacity'] = capacity
    msg['weight'] = weight
    msg['price'] = price
    table_result = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    context = {'table': 'tblbattery',
               'result': table_result['success'],
               'message': table_result['message'],
               'keys': table_result['keys'],
               'values': table_result['values']}
    return HttpResponse(json_utils.json_to_str(context), content_type='application/json')


def add_single_bat_table(request):
    name = request.POST['bat_name']
    type = request.POST['bat_type']
    volt = request.POST['bat_volt']
    capacity = request.POST['bat_capacity']
    discharge_rate = request.POST['bat_discharge_rate']
    weight = request.POST['bat_weight']
    price = request.POST['bat_price']

    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_ADD_SINGLE_TO_TABLE
    msg['table_name'] = 'tblbattery'
    msg['name'] = name
    msg['type'] = type
    msg['volt'] = volt
    msg['capacity'] = capacity
    msg['discharge_rate'] = discharge_rate
    msg['weight'] = weight
    msg['price'] = price
    table_result = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    context = {'table': 'tblbattery',
               'result': table_result['success'],
               'message': table_result['message'],
               'keys': table_result['keys'],
               'values': table_result['values']}
    return HttpResponse(json_utils.json_to_str(context), content_type='application/json')


def add_multi_bat_table(request):
    content = request.POST['content']

    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_ADD_MULTI_TO_TABLE
    msg['content'] = content
    msg['table_name'] = 'tblbattery'
    table_result = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    summery = ''
    for index, (result, message) in enumerate(table_result['summery']):
        if result:
            summery += 'Row number {} was added successfully\n'.format(index + 1)
        else:
            summery += 'Failed to insert row number {}: error is: {}\n'.format(index + 1, message)
    context = {'table': 'tblbattery',
               'summery': summery,
               'keys': table_result['keys'],
               'values': table_result['values']}
    return HttpResponse(json_utils.json_to_str(context), content_type='application/json')


def delete_bat_table(request):
    id = request.POST['bat_id']

    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_DELETE_FROM_TABLE
    msg['table_name'] = 'tblbattery'
    msg['id'] = id
    table_result = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    context = {'table': 'tblbattery',
                'result': table_result['success'],
               'message': table_result['message'],
               'keys': table_result['keys'],
               'values': table_result['values']}
    return HttpResponse(json_utils.json_to_str(context), content_type='application/json')


def get_prop_table(request):
    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_GET_TABLE
    msg['table_name'] = 'tblprops'
    table_result = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    context = {'table': 'tblprops',
               'result': table_result['success'],
               'keys': table_result['keys'],
               'values': table_result['values']}
    return HttpResponse(json_utils.json_to_str(context), content_type='application/json')


def prop_table_update(request):
    id = request.POST['prop_id']
    name = request.POST['prop_name']
    diameter = request.POST['prop_diameter']
    speed = request.POST['prop_speed']
    weight = request.POST['prop_weight']
    price = request.POST['prop_price']

    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_UPDATE_TABLE
    msg['table_name'] = 'tblprops'
    msg['id'] = id
    msg['name'] = name
    msg['diameter'] = diameter
    msg['speed'] = speed
    msg['weight'] = weight
    msg['price'] = price
    table_result = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    context = {'table': 'tblprops',
               'result': table_result['success'],
               'message': table_result['message'],
               'keys': table_result['keys'],
               'values': table_result['values']}
    return HttpResponse(json_utils.json_to_str(context), content_type='application/json')


def add_single_prop_table(request):
    name = request.POST['prop_name']
    diameter = request.POST['prop_diameter']
    speed = request.POST['prop_speed']
    weight = request.POST['prop_weight']
    price = request.POST['prop_price']

    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_ADD_SINGLE_TO_TABLE
    msg['table_name'] = 'tblprops'
    msg['name'] = name
    msg['diameter'] = diameter
    msg['speed'] = speed
    msg['weight'] = weight
    msg['price'] = price
    table_result = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    context = {'table': 'tblprops',
               'result': table_result['success'],
               'message': table_result['message'],
               'keys': table_result['keys'],
               'values': table_result['values']}
    return HttpResponse(json_utils.json_to_str(context), content_type='application/json')


def add_multi_prop_table(request):
    content = request.POST['content']

    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_ADD_MULTI_TO_TABLE
    msg['content'] = content
    msg['table_name'] = 'tblprops'
    table_result = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    summery = ''
    for index, (result, message) in enumerate(table_result['summery']):
        if result:
            summery += 'Row number {} was added successfully\n'.format(index + 1)
        else:
            summery += 'Failed to insert row number {}: error is: {}\n'.format(index + 1, message)
    context = {'table': 'tblprops',
               'summery': summery,
               'keys': table_result['keys'],
               'values': table_result['values']}
    return HttpResponse(json_utils.json_to_str(context), content_type='application/json')


def delete_prop_table(request):
    id = request.POST['prop_id']

    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_DELETE_FROM_TABLE
    msg['table_name'] = 'tblprops'
    msg['id'] = id
    table_result = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    context = {'table': 'tblprops',
                'result': table_result['success'],
               'message': table_result['message'],
               'keys': table_result['keys'],
               'values': table_result['values']}
    return HttpResponse(json_utils.json_to_str(context), content_type='application/json')


def get_drone_table(request):
    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_GET_TABLE
    msg['table_name'] = 'tbldrone'
    table_result = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    context = {'table': 'tbldrone',
               'result': table_result['success'],
               'keys': table_result['keys'],
               'values': table_result['values'],
               'motors': table_result['motors'],
               'bats': table_result['bats'],
               'props': table_result['props'],
               }
    return HttpResponse(json_utils.json_to_str(context), content_type='application/json')


def drone_table_update(request):
    id = request.POST['drone_id']
    motor_name = request.POST['motor_name']
    bat_name = request.POST['bat_name']
    prop_name = request.POST['prop_name']

    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_UPDATE_TABLE
    msg['table_name'] = 'tbldrone'
    msg['drone_id'] = id
    msg['motor_name'] = motor_name
    msg['bat_name'] = bat_name
    msg['prop_name'] = prop_name
    table_result = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    context = {'table': 'tbldrone',
               'result': table_result['success'],
               'message': table_result['message'],
               'keys': table_result['keys'],
               'values': table_result['values']}
    return HttpResponse(json_utils.json_to_str(context), content_type='application/json')