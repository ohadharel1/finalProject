from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.utils.safestring import mark_safe
import datetime
import collections
import json_utils

import controller
import config


class OrderedSet(collections.MutableSet):

    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:
            key, prev, next = self.map.pop(key)
            prev[2] = next
            next[1] = prev

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)

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
    drone_ids = OrderedSet()
    drone_ids.add('All')
    drone_states = OrderedSet()
    drone_states.add('All')
    try:
        success = flight_dict['success']
        del flight_dict['success']
    except:
        pass
    for key, value in flight_dict.items():
        try:
            start = datetime.datetime.strptime(value['start_flight_time'], "%Y-%m-%dT%H:%M:%S")
            value['start_flight_time'] = str(start)
            if value['end_flight_time']:
                end = datetime.datetime.strptime(value['end_flight_time'], "%Y-%m-%dT%H:%M:%S")
                value['duration'] = end - start
                value['end_flight_time'] = str(end)
            else:
                value['duration'] = 'N/A'
                value['end_flight_time'] = 'N/A'
        except Exception, e:
            print str(e)
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
    drone_ids = OrderedSet()
    drone_ids.add('All')
    drone_states = OrderedSet()
    drone_states.add('All')
    success = flight_dict['success']
    del flight_dict['success']
    for key, value in flight_dict.items():
        if value['end_flight_time']:
            value['start_flight_time'] = datetime.datetime.strptime(value['start_flight_time'], "%Y-%m-%dT%H:%M:%S")
            value['end_flight_time'] = datetime.datetime.strptime(value['end_flight_time'], "%Y-%m-%dT%H:%M:%S")
            value['duration'] = value['end_flight_time'] - value['start_flight_time']
        else:
            value['duration'] = 'N/A'
            value['start_flight_time'] = datetime.datetime.strptime(value['start_flight_time'], "%Y-%m-%dT%H:%M:%S")
            value['end_flight_time'] = None
        drone_ids.add(value['drone_num'])
        drone_states.add(value['state'])
        for sorted_key, sorted_value in current_sort_dict.items():
            if sorted_value:
                if sorted_value == 'All':
                    current_sort_dict[sorted_key] = None
                    break
                if sorted_key == 'duration':
                    try:
                        asked_duration = str_to_timedelta(str(sorted_value))
                    except:
                        current_sort_dict['duration'] = None
                        break
                    # actual_duration = str_to_timedelta(value[sorted_key])
                    if type(value[sorted_key]) is not datetime.timedelta or asked_duration > value[sorted_key]:
                        del sorted_res[key]
                        break
                elif sorted_key == 'start_flight_time':
                    try:
                        asked_start_time = datetime.datetime.strptime(str(sorted_value), '%Y-%m-%d')
                    except:
                        current_sort_dict['start_flight_time'] = None
                        break
                    if asked_start_time > value[sorted_key]:
                        del sorted_res[key]
                        break
                elif sorted_key == 'end_flight_time':
                    try:
                        asked_end_time = datetime.datetime.strptime(str(sorted_value), '%Y-%m-%d')
                    except:
                        current_sort_dict['end_flight_time'] = None
                        break
                    if not value[sorted_key] or asked_end_time < value[sorted_key]:
                        del sorted_res[key]
                        break
                elif str(value[sorted_key]) != str(sorted_value):
                    del sorted_res[key]
                    break
    context = {'result': sorted_res,
               'drone_ids': drone_ids,
               'drone_states': drone_states}
    template = loader.get_template('reviews/update_reviews.html')
    return HttpResponse(template.render(context, request))


def update_review2(request):
    global flight_dict, current_sort_dict
    key = request.POST['key']
    value = request.POST['value']
    current_sort_dict[key] = value
    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_GET_ALL_FLIGHTS
    flight_dict = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    drone_ids = OrderedSet()
    drone_ids.add('All')
    drone_states = OrderedSet()
    drone_states.add('All')
    success = flight_dict['success']
    del flight_dict['success']
    sorted_res = flight_dict.copy()
    for key, value in flight_dict.items():
        if value['end_flight_time']:
            value['start_flight_time'] = datetime.datetime.strptime(value['start_flight_time'], "%Y-%m-%dT%H:%M:%S")
            value['end_flight_time'] = datetime.datetime.strptime(value['end_flight_time'], "%Y-%m-%dT%H:%M:%S")
            value['duration'] = value['end_flight_time'] - value['start_flight_time']
        else:
            value['duration'] = 'N/A'
            value['start_flight_time'] = datetime.datetime.strptime(value['start_flight_time'], "%Y-%m-%dT%H:%M:%S")
            value['end_flight_time'] = 'N/A'
            sorted_res[key]['end_flight_time'] = 'N/A'
            sorted_res[key]['duration'] = 'N/A'
        drone_ids.add(value['drone_num'])
        drone_states.add(value['state'])
        for sorted_key, sorted_value in current_sort_dict.items():
            if sorted_value:
                if sorted_value == 'All':
                    current_sort_dict[sorted_key] = None
                    break
                if sorted_key == 'duration':
                    try:
                        asked_duration = str_to_timedelta(str(sorted_value))
                    except:
                        current_sort_dict['duration'] = None
                        break
                    # actual_duration = str_to_timedelta(value[sorted_key])
                    if type(value[sorted_key]) is not datetime.timedelta or asked_duration > value[sorted_key]:
                        del sorted_res[key]
                        break
                elif sorted_key == 'start_flight_time':
                    try:
                        asked_start_time = datetime.datetime.strptime(str(sorted_value), '%Y-%m-%d')
                    except:
                        current_sort_dict['start_flight_time'] = None
                        break
                    if asked_start_time > value[sorted_key]:
                        del sorted_res[key]
                        break
                elif sorted_key == 'end_flight_time':
                    try:
                        asked_end_time = datetime.datetime.strptime(str(sorted_value), '%Y-%m-%d')
                    except:
                        current_sort_dict['end_flight_time'] = None
                        break
                    if not value[sorted_key] or asked_end_time < value[sorted_key]:
                        del sorted_res[key]
                        break
                elif str(value[sorted_key]) != str(sorted_value):
                    del sorted_res[key]
                    break
    # context = {'result': sorted_res,
    #            'drone_ids': drone_ids,
    #            'drone_states': drone_states}
    # template = loader.get_template('reviews/update_reviews.html')
    return HttpResponse(json_utils.json_to_str(sorted_res), content_type='application/json')

def pop_up_modal(request):
    global flight_dict
    file_path = request.POST['file_path']
    is_log = bool(request.POST['is_log'])
    log = None
    # file_path = flight_dict[key]['log_file_path']
    try:
        with open(file_path, 'r') as log_file:
            log = log_file.read()
        title = 'This is the log selected'
    except:
        title = 'Log file not found'
        log = 'Maybe it was deleted...'
    context = {'title' : title,
               'body' : log}
    template = loader.get_template('reviews/update_modal.html')
    return HttpResponse(template.render(context, request))


def pop_up_report_modal(request):
    global flight_dict
    drone_num = int(request.POST['drone_num'])
    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_GET_DRONE_SUM_REPORT
    msg['drone_num'] = drone_num
    res = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    print res
    title = 'Report for drone number ' + str(drone_num)
    context = {'title': title,
               'query_res': res}
    template = loader.get_template('reviews/update_report_modal.html')
    return HttpResponse(template.render(context, request))


def get_flights_per_drone(request):
    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_FLIGHTS_PER_DRONE
    context = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    return HttpResponse(json_utils.json_to_str(context), content_type='application/json')


def get_errors_per_drone(request):
    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_ERRORS_PER_DRONE
    context = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    return HttpResponse(json_utils.json_to_str(context), content_type='application/json')


def get_all_errors(request):
    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_ALL_ERRORS
    context = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    return HttpResponse(json_utils.json_to_str(context), content_type='application/json')


def get_flights_per_month(request):
    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_GET_FLIGHTS_PER_MONTH
    context = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    return HttpResponse(json_utils.json_to_str(context), content_type='application/json')


def get_errors_per_month(request):
    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_GET_ERRORS_PER_MONTH
    context = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    return HttpResponse(json_utils.json_to_str(context), content_type='application/json')


def get_total_flight_time_per_drone(request):
    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_GET_TOTAL_FLIGHT_TIME_PER_DRONE
    context = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    return HttpResponse(json_utils.json_to_str(context), content_type='application/json')


def str_to_timedelta(time_str):
    try:
        t = datetime.datetime.strptime(time_str, "%M")
    except:
        try:
            t = datetime.datetime.strptime(time_str, "%M:%S")
        except:
            t = datetime.datetime.strptime(time_str, "%H:%M:%S")
    return datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)