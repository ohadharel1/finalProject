from django.conf.urls import url, include
from . import views

app_name = 'reviews'

urlpatterns = [
    url(r'^$', views.review, name='reviews'),
    url(r'^update_reviews/', views.update_review, name='update_reviews'),
    url(r'^pop_up_modal/', views.pop_up_modal, name='pop_up_modal'),
]
