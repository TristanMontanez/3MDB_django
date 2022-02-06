import time
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from database import Database

SQL_TABLE = 'customer_table'
SQL_COLUMNS = ['customer_key', 'customer_name', 'department']
DEPARTMENTS = ['ICING', 'ICING(DAILY)', 'QC', 'BREAD', 'BISCUIT', 'CANDY',
               'FORMULATION', 'WAREHOUSE', 'PACKING']


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


def history_view(request):
    start = time.time()
    database = Database()
    items, _ = database.read_from_database(sql_table='order_table',
                                           sql_columns=['order_key', 'order_date', 'customer_id',
                                                        'product_id', 'qty', 'total'],
                                           sql_filters={})
    columns = ['KEY', 'DATE ORDERED', 'CUSTOMER NAME', 'PRODUCT NAME', 'QTY', 'TOTAL']

    for item in items[1::]:
        item[1] = item[1].strftime('%B %d, %Y')

        customer_name, _ = database.read_from_database(sql_table='customer_table',
                                                       sql_columns=['customer_name'],
                                                       sql_filters={'customer_key': item[2]})
        item[2] = customer_name[1][0]

        product_name, _ = database.read_from_database(sql_table='product_table',
                                                      sql_columns=['product_name'],
                                                      sql_filters={'product_key': item[3]})
        item[3] = product_name[1][0]

    context = {'columns': columns, 'items': items[1::]}
    print(f'Read Time: {time.time() - start}')
    page = render(request, 'customers/purchase_history.html', context)
    print(f'Render: {time.time() - start}')
    return page


def customer_data(request):
    database = Database()
    items, _ = database.read_from_database(sql_table=SQL_TABLE,
                                           sql_columns=SQL_COLUMNS,
                                           sql_filters={})
    return JsonResponse({'data': items[1::]})


@csrf_exempt
def register_customer(request):
    database = Database()
    keys, _ = database.read_from_database(sql_table=SQL_TABLE,
                                          sql_columns=['customer_key'],
                                          sql_filters={})
    database.populate_db_product()
    max_key = 0
    for key in keys[1::]:
        key_str = key[0][9::].lstrip('0')
        key_int = int(key_str)
        if key_int > max_key:
            max_key = key_int

    if request.POST.get('customer_name') and request.POST.get('department'):
        query = database.insert_customer(customer_key=f'Customer_{str(max_key+1).zfill(4)}',
                                         customer_name=request.POST.get('customer_name'),
                                         department=request.POST.get('department'))
        return JsonResponse({'data': query})
    else:
        return JsonResponse({'data': 'ERROR IN REGISTER'})


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
    print(edit_row)
    database = Database()
    items, _ = database.read_from_database(sql_table=SQL_TABLE,
                                           sql_columns=SQL_COLUMNS,
                                           sql_filters={})
    columns = items[0]
    edited_row = json.loads(request.POST.get('customer_key'))
    sql_filters = {columns[0]: edited_row[0]}
    sql_update = {}
    if edited_row[2] not in DEPARTMENTS:
        return JsonResponse({'data': 'INVALID DEPARTMENT'})

    for i in range(1, len(columns)):
        sql_update[columns[i]] = edited_row[i]

    query = database.edit_item(sql_table=SQL_TABLE,
                               sql_filters=sql_filters,
                               sql_updates=sql_update)
    print(query)

    return JsonResponse({'data': query})
