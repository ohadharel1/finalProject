from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

import controller
import config


def review(request):
    msg = {}
    msg['cmd'] = 'query'
    msg['query_num'] = config.QUERY_GET_ALL_FLIGHTS
    res = controller.get_instance().get_system_server().send_msg(msg, blocking=True)
    drone_ids = set()
    for key, value in res.items():
        drone_ids.add(value['drone_num'])
    context = {'result': res,
               'drone_ids': drone_ids}
    template = loader.get_template('reviews/reviews.html')
    return HttpResponse(template.render(context, request))