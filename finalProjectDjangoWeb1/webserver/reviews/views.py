from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

import controller


def review(request):
    template = loader.get_template('reviews/reviews.html')
    context = {'fd': 'fsd'}
    return HttpResponse(template.render(context, request))