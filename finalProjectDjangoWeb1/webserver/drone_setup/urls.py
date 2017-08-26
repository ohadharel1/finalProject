from django.conf.urls import url, include
from . import views

app_name = 'drone_setup'

urlpatterns = [
    url(r'^$', views.drone_setup, name='drone_setup'),
    url(r'^progress/', views.progress_bar, name='progress_bar'),
    url(r'^setup_result/', views.setup_result, name='setup_result'),
    url(r'^setup_params/', views.setup_params, name='setup_params')
]