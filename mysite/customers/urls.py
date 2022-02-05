from django.urls import path

from . import views

urlpatterns = [
    path('', views.customers_view, name='customers_view')
]