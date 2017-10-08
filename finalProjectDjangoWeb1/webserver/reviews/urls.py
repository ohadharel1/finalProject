from django.conf.urls import url, include
from . import views

app_name = 'reviews'

urlpatterns = [
    url(r'^$', views.review, name='reviews'),
    url(r'^update_reviews/', views.update_review2, name='update_reviews'),
    url(r'^pop_up_modal/', views.pop_up_modal, name='pop_up_modal'),
    url(r'^pop_up_report_modal/', views.pop_up_report_modal, name='pop_up_modal'),
    url(r'^get_flights_per_drone/', views.get_flights_per_drone, name='get_flights_per_drone'),
    url(r'^get_errors_per_drone/', views.get_errors_per_drone, name='get_flights_per_drone'),
    url(r'^get_all_errors/', views.get_all_errors, name='get_all_errors'),
    url(r'^get_flights_per_month/', views.get_flights_per_month, name='get_flights_per_month'),
    url(r'^get_errors_per_month/', views.get_errors_per_month, name='get_errors_per_month'),
]
