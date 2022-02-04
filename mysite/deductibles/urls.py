from django.urls import path

from . import views

urlpatterns = [
    path('', views.deductibles_view, name='deductibles_view'),
    path('deductible_data', views.deductibles_data, name='deductibles_data'),
    path('delete_rows', views.delete_rows, name='delete_rows'),
    path('edit_row', views.edit_row, name='edit_row')
]