from django.shortcuts import render
import time

from database import Database


def customers_view(request):
    start = time.time()

    print(f'Read Time: {time.time() - start}')
    page = render(request, 'customers/customers_view.html')
    print(f'Render: {time.time() - start}')
    return page