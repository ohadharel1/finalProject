from django.conf.urls import url, include
from . import views

app_name = 'management'

urlpatterns = [
    url(r'^$', views.manage, name='management'),
    url(r'^get_table/', views.get_table, name='get_table'),
    url(r'^table_update/', views.table_update, name='table_update'),
]
