from django.urls import path

from . import views

urlpatterns = [
    path('', views.products_view, name='products_view'),
    path('product_data', views.product_data, name='product_data'),
    path('delete_rows', views.delete_rows, name='delete_rows'),
    path('edit_row', views.edit_row, name='edit_row')
]