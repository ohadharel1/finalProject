from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

import controller


def manage(request):
    template = loader.get_template('management/management.html')
    context = {'fd': 'fsd'}
    return HttpResponse(template.render(context, request))