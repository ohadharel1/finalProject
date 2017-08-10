from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import sys
import controller
import logging
import config
import collections

# Create your views here.


def drone_setup(request):
    template = loader.get_template('drone_setup/setup_initiate.html')
    context = {'arg': 'yes'}
    return HttpResponse(template.render(context, request))


def progress_bar(request):
    template = loader.get_template('drone_setup/progress_bar.html')
    context = {'arg': 'yes'}
    return HttpResponse(template.render(context, request))


def setup_result(request):
    context = collections.OrderedDict()
    context['context'] = collections.OrderedDict()
    dict = controller.get_instance().get_options()
    for i in range(1, len(dict) + 1):
        option = 'option ' + str(i)
        context['context'][option] = dict[option]
    print 'got options: ' + str(context)
    template = loader.get_template('drone_setup/setup_result.html')
    return HttpResponse(template.render(context, request))


def setup_params(request):
    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_GET_SETUP_SUGGESTIONS
    msg['drone_type'] = request.POST['drone_type']
    msg['max_size'] = request.POST['SizeField']
    msg['min_payload'] = request.POST['PayloadField']
    msg['min_time'] = request.POST['TimeofworkField']
    msg['min_range'] = request.POST['RangeField']
    msg['max_price'] = request.POST['PriceField']
    msg['iterations'] = request.POST['Iterations']
    controller.get_instance().get_system_server().send_msg(msg)
    template = loader.get_template('drone_setup/progress_bar.html')
    context = {'arg': 'yes'}
    return HttpResponse(template.render(context, request))