from django.conf.urls import url, include
from . import views

app_name = 'reviews'

urlpatterns = [
    url(r'^$', views.review, name='reviews'),
]
