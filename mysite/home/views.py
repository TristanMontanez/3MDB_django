import json
from datetime import date

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from database import Database

PRODUCT_TABLE = 'product_table'
CUSTOMER_TABLE = 'customer_table'
ORDER_TABLE = 'order_table'

DATABASE = Database()
PRODUCT_DATA, _ = DATABASE.read_from_database(sql_table=PRODUCT_TABLE,
                                              sql_columns=['product_name'],
                                              sql_filters={})
CUSTOMER_DATA, _ = DATABASE.read_from_database(sql_table=CUSTOMER_TABLE,
                                               sql_columns=['customer_name'],
                                               sql_filters={})


def home_view(request):
    product_names = []
    for name in PRODUCT_DATA[1::]:
        product_names.append(name[0])

    customer_names = []
    for name in CUSTOMER_DATA[1::]:
        customer_names.append(name[0])

    context = {'product_names': product_names, 'customer_names': customer_names}
    return render(request, 'home/home.html', context)


@csrf_exempt
def submit_order(request):
    order_data = json.loads(request.POST.get('order_data'))
    customer_name = order_data.get('customer_name')
    customer_id, _ = DATABASE.read_from_database(sql_filters={'customer_name': customer_name},
                                                 sql_columns=['customer_key'],
                                                 sql_table=CUSTOMER_TABLE)
    customer_id = customer_id[1][0]
    orders = {}
    for order in order_data.get('order'):
        order_dict = {}
        product_name = list(order.keys())[0]
        qty = int(order.get(product_name))
        product_data, _ = DATABASE.read_from_database(sql_filters={'product_name': product_name},
                                                      sql_columns=['product_key', 'price'],
                                                      sql_table=PRODUCT_TABLE)
        product_id = product_data[1][0]
        price = product_data[1][1]
        order_dict[product_id] = [qty, price*qty]
        orders.update(order_dict)

    DATABASE.insert_orders(customer_id=customer_id,
                           orders=orders)

    return JsonResponse({'data': request.POST.get('order_data')})


def recent_orders(request):
    order_data, _ = DATABASE.read_from_database(sql_table=ORDER_TABLE,
                                                sql_columns=['customer_id', 'total', 'order_date'],
                                                sql_filters={'order_date': date.today()})
    recent = {}
    customer_names = []
    for order in order_data[1::]:
        print(order)
        customer_name, _ = DATABASE.read_from_database(sql_table=CUSTOMER_TABLE,
                                                       sql_columns=['customer_name'],
                                                       sql_filters={'customer_key': order[0]})
        customer_name = customer_name[1][0]
        if customer_name in customer_names:
            recent[customer_name] = recent[customer_name] + order[1]
        else:
            customer_names.append(customer_name)
            recent[customer_name] = order[1]

    print(f'Recent Orders: {recent}')
    table_data = []
    for key in recent:
        table_data.append([key, recent[key], date.today()])

    return JsonResponse({'data': table_data})


@csrf_exempt
def get_price(request):
    order_data = json.loads(request.POST.get('order_data'))
    product_totals = []
    print(f'order_data: {order_data}')
    for order in order_data.get('order'):
        product_name = list(order.keys())[0]
        if product_name:
            qty = int(order.get(product_name))
            product_price, _ = DATABASE.read_from_database(sql_filters={'product_name': product_name},
                                                           sql_columns=['price'],
                                                           sql_table=PRODUCT_TABLE)
            product_price = product_price[1][0]
            if product_price:
                total = int(product_price)*qty
                product_totals.append(total)

    return JsonResponse({'data': product_totals, 'total': sum(product_totals)})
