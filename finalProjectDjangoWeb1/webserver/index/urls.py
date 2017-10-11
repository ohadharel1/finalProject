from django.conf.urls import url, include
from . import views

app_name = 'index'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^get_flight_status/', views.get_flight_status, name='get_flight_status'),
]