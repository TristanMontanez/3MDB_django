from django.urls import path

from . import views

urlpatterns = [
    path('', views.customers_view, name='customers_view'),
    path('purchase_history', views.history_view, name='purchase_history'),
    path('customer_data', views.customer_data, name='customer_data'),
    path('register_customer', views.register_customer, name='register_customer'),
    path('delete_rows', views.delete_rows, name='delete_rows'),
    path('edit_row', views.edit_row, name='edit_row')
]
