from django.conf.urls import url, include
from . import views

app_name = 'management'

urlpatterns = [
    url(r'^$', views.manage, name='management'),
    url(r'^get_table/', views.get_table, name='get_table'),
    url(r'^table_update/', views.table_update, name='table_update'),
    url(r'^motor_table_update/', views.motor_table_update, name='motor_table_update'),
    url(r'^get_motor_table/', views.get_motor_table, name='get_motor_table'),
    url(r'^add_single_motor_table/', views.add_single_motor_table, name='add_single_motor_table'),
    url(r'^add_multi_motor_table/', views.add_multi_motor_table, name='add_multi_motor_table'),
    url(r'^delete_motor_table/', views.delete_motor_table, name='delete_motor_table'),
    url(r'^bat_table_update/', views.bat_table_update, name='bat_table_update'),
    url(r'^get_bat_table/', views.get_bat_table, name='get_bat_table'),
    url(r'^add_single_bat_table/', views.add_single_bat_table, name='add_single_bat_table'),
    url(r'^add_multi_bat_table/', views.add_multi_bat_table, name='add_multi_bat_table'),
    url(r'^delete_bat_table/', views.delete_bat_table, name='delete_bat_table'),
    url(r'^prop_table_update/', views.prop_table_update, name='prop_table_update'),
    url(r'^get_prop_table/', views.get_prop_table, name='get_prop_table'),
    url(r'^add_single_prop_table/', views.add_single_prop_table, name='add_single_prop_table'),
    url(r'^add_multi_prop_table/', views.add_multi_prop_table, name='add_multi_prop_table'),
    url(r'^delete_prop_table/', views.delete_prop_table, name='delete_prop_table'),
    url(r'^drone_table_update/', views.drone_table_update, name='prop_table_update'),
    url(r'^get_drone_table/', views.get_drone_table, name='get_prop_table'),
]
