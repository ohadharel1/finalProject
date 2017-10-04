from django.conf.urls import url, include
from . import views

app_name = 'flight_monitor'

urlpatterns = [
    url(r'^$', views.flight_monitor, name='flight_monitor'),
    url(r'^get_current_flights$', views.update_flight_table, name='get_current_flights'),
    url(r'^flight_monitor_js$', views.flight_monitor_js, name='flight_monitor_js'),
    url(r'^pop_up_modal_header', views.pop_up_modal_header, name='pop_up_modal_header'),
    url(r'^pop_up_modal_body', views.pop_up_modal_body, name='pop_up_modal_body'),
    url(r'^pop_up_modal$', views.pop_up_modal, name='pop_up_modal'),
    url(r'^pop_up_modal_close', views.pop_up_modal_close, name='pop_up_modal_close'),
    url(r'^save_comment', views.save_comment, name='save_comment'),
]