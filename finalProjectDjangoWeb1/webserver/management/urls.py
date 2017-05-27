from django.conf.urls import url, include
from . import views

app_name = 'management'

urlpatterns = [
    url(r'^$', views.manage, name='management'),
]
