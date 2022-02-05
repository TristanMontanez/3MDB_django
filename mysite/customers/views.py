import time
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from database import Database

SQL_TABLE = 'customer_table'
SQL_COLUMNS = ['customer_key', 'customer_name', 'department']


def customers_view(request):
    start = time.time()
    database = Database()
    items, _ = database.read_from_database(sql_table=SQL_TABLE,
                                           sql_columns=SQL_COLUMNS,
                                           sql_filters={})
    columns = []
    for item in items[0]:
        columns.append(item.upper().replace('_', ' '))

    context = {'columns': columns}
    print(f'Read Time: {time.time() - start}')
    page = render(request, 'customers/customers_view.html', context)
    print(f'Render: {time.time() - start}')
    return page


def customer_data(request):
    database = Database()
    items, _ = database.read_from_database(sql_table=SQL_TABLE,
                                           sql_columns=SQL_COLUMNS,
                                           sql_filters={})
    print(items)
    return JsonResponse({'data': items[1::]})
