from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import sys
import controller
import logging
import config
import collections

import json_utils

# Create your views here.


setup_result_context = {}

def drone_setup(request):
    template = loader.get_template('drone_setup/setup_initiate.html')
    context = {'arg': 'yes'}
    return HttpResponse(template.render(context, request))


def progress_bar(request):
    template = loader.get_template('drone_setup/progress_bar.html')
    context = {'arg': 'yes'}
    return HttpResponse(template.render(context, request))


def setup_result(request):
    global setup_result_context
    template = loader.get_template('drone_setup/setup_result.html')
    return HttpResponse(template.render(setup_result_context, request))


def setup_params(request):
    global setup_result_context
    context = collections.OrderedDict()
    context['context'] = collections.OrderedDict()
    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_GET_SETUP_SUGGESTIONS
    msg['drone_type'] = request.POST['drone_type']
    msg['max_size'] = request.POST['max_size']
    msg['min_payload'] = request.POST['min_payload']
    msg['min_time'] = request.POST['min_time']
    msg['min_range'] = request.POST['min_range']
    msg['max_price'] = request.POST['max_price']
    msg['iterations'] = request.POST['iterations']
    setup_result = controller.get_instance().get_system_server().send_msg(msg, True)
    for i in range(1, len(setup_result) + 1):
        option = 'option ' + str(i)
        context['context'][option] = setup_result[option]
    setup_result_context = context
    return_context = {'success': True}
    return HttpResponse(json_utils.json_to_str(return_context), content_type='application/json')