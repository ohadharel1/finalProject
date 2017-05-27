"""webserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import controller

controller.get_instance()


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', include('index.urls', namespace="index")),
    url(r'^flight_monitor/', include('flight_monitor.urls', namespace="flight_monitor")),
    url(r'^drone_setup/', include('drone_setup.urls', namespace="drone_setup")),
    url(r'^reviews/', include('reviews.urls', namespace="reviews")),
]
