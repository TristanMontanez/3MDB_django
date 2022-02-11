from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('submit_order', views.submit_order, name='submit_order'),
    path('recent_orders', views.recent_orders, name='recent_orders'),
    path('get_price', views.get_price, name='get_price')
]