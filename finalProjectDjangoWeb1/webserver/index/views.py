from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

import controller


def index(request):
    template = loader.get_template('index/index.html')
    context = controller.get_instance().get_connection_status()
    return HttpResponse(template.render(context, request))