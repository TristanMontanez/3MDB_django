import time
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from database import Database

SQL_TABLE = 'product_table'
SQL_COLUMNS = ['product_key', 'product_name', 'price']


def products_view(request):
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
        print(query)

    return JsonResponse({'data': query})


@csrf_exempt
def edit_row(request):
    database = Database()
    items, _ = database.read_from_database(sql_table=SQL_TABLE,
                                           sql_columns=SQL_COLUMNS,
                                           sql_filters={})
    columns = items[0]
    edited_row = json.loads(request.POST.get('product_key'))
    sql_filters = {columns[0]: edited_row[0]}
    sql_update = {}
    for i in range(1, len(columns)):
        sql_update[columns[i]] = edited_row[i]

    query = database.edit_item(sql_table=SQL_TABLE,
                               sql_filters=sql_filters,
                               sql_updates=sql_update)
    print(query)

    return JsonResponse({'data': query})


@csrf_exempt
def add_product(request):
    database = Database()
    keys, _ = database.read_from_database(sql_table=SQL_TABLE,
                                          sql_columns=['product_key'],
                                          sql_filters={})
    database.populate_db_product()
    max_key = 0
    for key in keys[2::]:
        key_str = key[0][8::].lstrip('0')
        key_int = int(key_str)
        if key_int > max_key:
            max_key = key_int
    if request.POST.get('product_name') and request.POST.get('price'):
        query = database.insert_product(product_key=f'Product_{str(max_key+1).zfill(4)}',
                                        product_name=request.POST.get('product_name'),
                                        price=request.POST.get('price'))
        return JsonResponse({'data': query})
    else:
        return JsonResponse({'data': 'ERROR IN REGISTER'})
