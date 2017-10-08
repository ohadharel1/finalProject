from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.core.urlresolvers import reverse, reverse_lazy, resolve
from django.test.client import RequestFactory
from django.conf import settings
import controller
import config
import timer
import collections

import json_utils

# Create your views here.

active_flights = {}
need_refresh = False
num_of_seconds_to_blink = 1 + 3  # 3 seconds
timers = {}
sessions = {}
default_popup_context = {'header': 'Loading... Please Wait',
                         'body': None}


def flight_monitor_js(request):
    template = loader.get_template('flight_monitor/flight_monitor_js.js')
    context = {}
    return HttpResponse(template.render(context, request))


def update_flights_dict():
    global active_flights, timers
    if active_flights is not None and 'status' in active_flights:
        for key, value in active_flights['status'].items():
            print 'value is: ' + str(value)
            print 'blink is at: ' + str(value['blink'])
            if value['blink'] > 0:
                value['blink'] -= 1
            value['time_elapsed'] = timers[key].get_time()


def update_flight_table(request):
    global active_flights, need_refresh
    controller.get_instance().set_current_page(config.CURRENT_PAGE_FLIGHT_MONITOR)
    template = loader.get_template('flight_monitor/flight_monitor_table_update.html')
    update_flights_dict()
    context = active_flights
    print 'active_flights refresh: ' + str(context)
    return render(request, 'flight_monitor/flight_monitor_table_update.html', context)


def pop_up_modal(request):
    global active_flights, sessions
    drone_num = int(request.POST['drone_num'])
    if not request.session.session_key:
        request.session.save()
    session_id = request.session.session_key
    sessions[session_id] = {'drone_num': drone_num,
                            'context': None}
    return HttpResponse(status=444)


def pop_up_modal_header(request):
    global active_flights, default_popup_context, sessions
    session_id = request.session.session_key
    context = default_popup_context.copy()
    template = loader.get_template('flight_monitor/pop_up_modal_title.html')
    try:
        if sessions[session_id]['drone_num'] < 256:
            context['header'] = 'log for drone number: ' + str(sessions[session_id]['drone_num'])
            sessions[session_id]['context'] = context
    finally:
        return HttpResponse(template.render(context, request))


def pop_up_modal_body(request):
    global active_flights, default_popup_context, sessions
    session_id = request.session.session_key
    context = default_popup_context.copy()
    template = loader.get_template('flight_monitor/pop_up_modal_body.html')
    try:
        if sessions[session_id]['drone_num'] < 256:
            log = 'ERROR IN LOG FILE'
            if 'status' in active_flights:
                for key, value in active_flights['status'].items():
                    if value['drone_num'] == sessions[session_id]['drone_num']:
                        log_path = value['log_path']
                        with open(log_path, 'r') as log_file:
                            log = log_file.read()
                            break
                context['body'] = log
                sessions[session_id]['context'] = context
    finally:
        return HttpResponse(template.render(context, request))


def pop_up_modal_close(request):
    global active_flights, sessions, default_popup_context
    session_id = request.session.session_key
    template = loader.get_template('flight_monitor/flight_monitor.html')
    try:
        se = sessions
        de = default_popup_context
        sessions[session_id]['drone_num'] = 300
        sessions[session_id]['context'] = default_popup_context.copy()
    finally:
        return HttpResponse(template.render(default_popup_context.copy(), request))


def flight_monitor(request):
    global active_flights, need_refresh
    controller.get_instance().set_current_page(config.CURRENT_PAGE_FLIGHT_MONITOR)
    template = loader.get_template('flight_monitor/flight_monitor.html')
    update_flights_dict()
    context = active_flights
    print 'active_flights refresh: ' + str(context)
    return HttpResponse(template.render(context, request))


def refresh_active_flights(flight_status):
    global active_flights, num_of_seconds_to_blink, timers
    if type(flight_status) is dict and 'status' in flight_status:
        active_flights = flight_status
        for key, value in active_flights['status'].items():
            if value['is_updated']:
                value['blink'] = num_of_seconds_to_blink
            if key not in timers or value['cmd'] == 'takeoff':
                timers[key] = timer.Timer(value['start_time'])
            if value['cmd'] == 'landed':
                timers[key].stop_timer()
            value['time_elapsed'] = timers[key].get_time()
        print 'got new flights'


def save_comment(request):
    global active_flights
    try:
        drone_id = int(request.POST['drone_id'])
        comment = request.POST['comment']
        start_time = None
        for key, value in active_flights['status'].items():
            if value['drone_num'] == drone_id:
                start_time = value['start_time']
                break
        response = {'success': False}
        if not start_time or not comment:
            return HttpResponse(json_utils.json_to_str(response), content_type='application/json')
        else:
            msg = {}
            msg['cmd'] = 'query'
            msg['query_num'] = config.QUERY_SAVE_FLIGHT_COMMENT
            msg['drone_id'] = drone_id
            msg['comment'] = comment
            msg['start_time'] = start_time
            result = controller.get_instance().get_system_server().send_msg(msg, blocking=False)
            return HttpResponse(json_utils.json_to_str(response), content_type='application/json')
    except Exception, e:
        print e
