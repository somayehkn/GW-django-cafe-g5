from django.shortcuts import render
from .models import *
import json
from django.http import JsonResponse

# Create your views here.

def checkout_page (request):
    context = request.session['items_json_data']
    return render(request, 'customer/checkout_page.html',context = {"context" : context})

def home(request):
    records = Category.objects.all()
    context = [[]]
    for item in records:
        context[-1].append(item)
        if len(context[-1])==2:
            context.append([])
    return render(request, 'index.html', {'data_from_db':context})

def menu(request):
    category = request.GET.get('cat')
    category = Category.objects.get(name=category)
    category_items = Item.objects.filter(category=category)
    records = Category.objects.all()
    session_data = {}
    if "items_json_data" in  request.session.keys():
        for key, value in request.session['items_json_data'].items() :
            if key in [item.name for item in category_items]:
                session_data[key] = value
    for item in category_items:
        if item.name not in session_data.keys():
            session_data[item.name] = {
                "item_unit_price": item.unitprice,
                "item_quantity": 0,
                "item_total_price": 0
            }           
    return render(request, 'menu.html', {'category_items':category_items,
                                         'categories':records,
                                         'selected_category':category,
                                         'session_data': session_data
                                         })

def save_items_to_session(request):
    if request.method == 'POST':
        try:
            json_data : dict = json.loads(request.body.decode('utf-8'))
            print("test2", json_data)

            if 'items_json_data' in request.session:
                session_data : dict = request.session['items_json_data']
                print("test3", session_data)
                for key, value in json_data.items():
                    session_data[key] = value
                request.session['items_json_data'] = session_data
            else:
                request.session['items_json_data'] = json_data

            print("test1", request.session['items_json_data'])

            if request.session['items_json_data'] == {}:
                return JsonResponse({'success': True, 'empty': True})
            return JsonResponse({'success': True, 'empty': False})
            
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'خطا در تحلیل JSON'})
    else:
        return JsonResponse({'error': 'فقط درخواست‌های POST مورد پذیرش هستند'})


def shoping_cart(request):
    return render(request,'customer/shoping-cart.html',context={"data": request.session['items_json_data']})

def table_rigester(request):
    tables = Table.objects.all()
    return render(request,'customer/table-rigester.html',context={"tables": tables})


def register_order(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            items_json_data = request.session['items_json_data']
            table = Table.objects.get(table_number = json_data["tableNumber"])
            print(table.table_number, table.capacity)
            print("ffffffffffff", request.session['items_json_data'])


            customer_order = Customer_order(
                description = "", 
                table_number = table,
                total_price = sum([item["item_total_price"] for item in items_json_data.values()])
            )
            customer_order.save()

            for key, value in items_json_data.items():
                if key != "table_number":
                    order_item = Order_item(customer_order = customer_order)
                    order_item.item = Item.objects.get(name=key)
                    order_item.count = value["item_quantity"]
                    order_item.save()

            request.session.flush()
            
            return JsonResponse({'message': 'اطلاعات با موفقیت ذخیره شدند'})

        except json.JSONDecodeError as e:
                return JsonResponse({'error': 'خطا در تحلیل JSON'})
    else:
        return JsonResponse({'error': 'فقط درخواست‌های POST مورد پذیرش هستند'})


    


