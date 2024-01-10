from django.shortcuts import render
from .models import *
import json
from django.http import JsonResponse

# Create your views here.

def is_session_defined(request):
    return "items_json_data" in request.session.keys()

def home(request):
    return render(request, 'customer/index.html', context={})

def checkout_page (request):
    context = request.session['items_json_data']
    return render(request, 'customer/checkout_page.html',context = {"context" : context})

def categories(request):
    records = Category.objects.all()
    context = [[]]
    for item in records:
        context[-1].append(item)
        if len(context[-1])==2:
            context.append([])
    return render(request, 'customer/categories.html', {'data_from_db':context})

def menu(request , foo):
    selected_category = Category.objects.get(name = foo)
    all_cats = Category.objects.all()
    items = selected_category.item_set.all()
    if (searchStr := request.GET.get("search")) is not None:
        items = items.filter(name__contains = searchStr)
    item_dict = {}
    for item in items:
        if is_session_defined(request):
            session_data = request.session['items_json_data']
            if item.name in session_data.keys():
                item_dict[item.name] = session_data[item.name]
            else:
                item_dict[item.name] =  {
                    "item_unit_price": item.unitprice,
                    "item_quantity": 0,
                    "item_total_price": 0,
                    "image" : item.image
                }  
        else:
            item_dict[item.name] =  {
                "item_unit_price": item.unitprice,
                "item_quantity": 0,
                "item_total_price": 0,
                "image" : item.image
            }          
    return render(request, 'customer/menu.html', {'selected_category':selected_category,
                                         'item_dict': item_dict,
                                         'all_cats' : all_cats
                                         })

def save_menu_items_to_session(request):
    if request.method == 'POST':
        try:
            json_data : dict = json.loads(request.body.decode('utf-8'))

            if not 'items_json_data' in request.session:
                print("test")
                request.session['items_json_data'] = {}
            session_data : dict = request.session['items_json_data']
            for key, value in json_data.items():
                if (value['item_quantity'] == 0):
                    if (key in session_data):
                        session_data.pop(key)
                else:
                    session_data[key] = value
            request.session['items_json_data'] = session_data
            print(request.session['items_json_data'] == {})



            if request.session['items_json_data'] == {}:
                return JsonResponse({'success': True, 'empty': True})
            return JsonResponse({'success': True, 'empty': False})
            
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'خطا در تحلیل JSON'})
    else:
        return JsonResponse({'error': 'فقط درخواست‌های POST مورد پذیرش هستند'})
    
def save_cart_items_to_session(request):
    if request.method == 'POST':
        try:
            request.session.flush()
            json_data : dict = json.loads(request.body.decode('utf-8'))
            request.session['items_json_data'] = json_data

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


            customer_order = Customer_order(
                description = "", 
                table_number = table,
                total_price = sum([item["item_total_price"] for item in items_json_data.values()]),
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


    


