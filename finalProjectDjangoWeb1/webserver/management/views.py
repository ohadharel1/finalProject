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
    id = int(request.POST['id'])
    name = request.POST['name']
    kv = float(request.POST['kv'])
    weight = float(request.POST['weight'])
    price = float(request.POST['price'])

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
    id = int(request.POST['motor_id'])
    name = request.POST['motor_name']
    kv = float(request.POST['motor_kv'])
    weight = float(request.POST['motor_weight'])
    price = float(request.POST['motor_price'])

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
    id = int(request.POST['bat_id'])
    name = request.POST['bat_name']
    type = request.POST['bat_type']
    volt = float(request.POST['bat_volt'])
    discharge_rate = float(request.POST['bat_discharge_rate'])
    capacity = float(request.POST['bat_capacity'])
    weight = float(request.POST['bat_weight'])
    price = float(request.POST['bat_price'])

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
    context = {'table': 'tblmotor',
               'result': table_result['success'],
               'message': table_result['message'],
               'keys': table_result['keys'],
               'values': table_result['values']}
    return HttpResponse(json_utils.json_to_str(context), content_type='application/json')