import time
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from database import Database
# Create your views here.

SQL_TABLE = 'test_table'
SQL_COLUMNS = ['full_name', 'age', 'position', 'office']


def products_view(request):
    start = time.time()
    database = Database()
    items, _ = database.read_from_database(sql_table=SQL_TABLE,
                                           sql_columns=SQL_COLUMNS,
                                           sql_filters={})
    context = {'table_labels': items[0]}
    print(f'Read Time: {time.time() - start}')
    page = render(request, 'products/products_view.html', context)
    print(f'Render: {time.time() - start}')
    return page


def product_data(request):
    database = Database()
    items, _ = database.read_from_database(sql_table=SQL_TABLE,
                                           sql_columns=SQL_COLUMNS,
                                           sql_filters={})

    return JsonResponse({'data': items[1::]})


@csrf_exempt
def delete_rows(request):
    database = Database()
    items, _ = database.read_from_database(sql_table=SQL_TABLE,
                                           sql_columns=SQL_COLUMNS,
                                           sql_filters={})
    columns = items[0]
    query = ''
    rows = json.loads(request.POST.get('rows'))
    for row in rows:
        sql_filters = {}
        for i in range(len(row)):
            sql_filters[columns[i]] = row[i]
        query = database.delete_item(sql_filters=sql_filters,
                                     sql_table=SQL_TABLE)

    return JsonResponse({'data': query})


@csrf_exempt
def edit_row(request):
    return JsonResponse({'data': 'W'})
