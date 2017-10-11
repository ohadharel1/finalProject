from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

import controller
import json_utils


def index(request):
    template = loader.get_template('index/index.html')
    context = controller.get_instance().get_connection_status()
    return HttpResponse(template.render(context, request))


def get_flight_status(request):
    flights = controller.get_instance().get_flight_msg()
    return HttpResponse(json_utils.json_to_str(flights), content_type='application/json')