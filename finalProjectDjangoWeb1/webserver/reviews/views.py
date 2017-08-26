from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

import controller
import config


flight_dict = None
current_sort_dict = \
{
    'drone_num' : None,
    'state' : None,
    'start_flight_time' : None,
    'end_flight_time' : None,
    'duration' : None
}


def review(request):
    global flight_dict
    if 'drone_num' in request.POST:
        drone_num = request.POST['drone_num']
    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_GET_ALL_FLIGHTS
    flight_dict = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    drone_ids = set()
    drone_states = set()
    for key, value in flight_dict.items():
        value['start_flight_time'] = str(value['start_flight_time']).replace('T', '  ')
        drone_ids.add(value['drone_num'])
        drone_states.add(value['state'])
    context = {'result': flight_dict,
               'drone_ids': drone_ids,
               'drone_states': drone_states}
    template = loader.get_template('reviews/reviews.html')
    return HttpResponse(template.render(context, request))


def update_review(request):
    global flight_dict, current_sort_dict
    key = request.POST['key']
    value = request.POST['value']
    current_sort_dict[key] = value
    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_GET_ALL_FLIGHTS
    flight_dict = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    sorted_res = flight_dict.copy()
    drone_ids = set()
    drone_states = set()
    for key, value in flight_dict.items():
        value['start_flight_time'] = str(value['start_flight_time']).replace('T', '  ')
        drone_ids.add(value['drone_num'])
        drone_states.add(value['state'])
        for sorted_key, sorted_value in current_sort_dict.items():
            if sorted_value and str(value[sorted_key]) != str(sorted_value):
                del sorted_res[key]
                break
    context = {'result': sorted_res,
               'drone_ids': drone_ids,
               'drone_states': drone_states}
    template = loader.get_template('reviews/update_reviews.html')
    return HttpResponse(template.render(context, request))


def pop_up_modal(request):
    global flight_dict
    key = request.POST['file_path']
    is_log = bool(request.POST['is_log'])
    log = None
    file_path = flight_dict[key]['log_file_path']
    with open(file_path, 'r') as log_file:
        log = log_file.read()
    title = 'This is the log selected'
    context = {'title' : title,
               'body' : log}
    template = loader.get_template('reviews/update_modal.html')
    return HttpResponse(template.render(context, request))
