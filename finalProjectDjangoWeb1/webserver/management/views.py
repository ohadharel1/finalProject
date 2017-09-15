from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

import controller
import config
import json_utils


def manage(request):
    template = loader.get_template('management/management.html')
    table = 'tblmotor'
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
               'alert': table_result['success'],
               'alert_display': True,
               'keys': table_result['keys'],
               'values': table_result['values']}
    return HttpResponse(json_utils.json_to_str(context), content_type='application/json')