from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('submit_order', views.submit_order, name='submit_order')
]