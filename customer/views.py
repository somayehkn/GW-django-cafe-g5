from django.shortcuts import render,redirect
from .models import Category, Item,Customer_order
import json
from django.http import JsonResponse
from django.views import View
from django.urls import reverse

# Create your views here.

def checkout_page (request):
       
    return render(request, 'customer/checkout_page.html',context ={} )

def home (request):
    records = Category.objects.all()
    context = [[]]
    for item in records:
        context[-1].append(item)
        if len(context[-1])==2:
            context.append([])
        print(context)
    
    return render(request, 'index.html', {'data_from_db':context})

def menu(request):
    category = request.GET.get('cat')
    category = Category.objects.get(name=category)
    category_items = Item.objects.filter(category=category)
    records = Category.objects.all()
    if  'items_json_data' in request.session:
        data = request.session['items_json_data']
        return render(request, 'menu.html', {'category_items':category_items,
                                         'categories':records,
                                         'selected_category':category,
                                         'data': data})
    return render(request, 'menu.html', {'category_items':category_items,
                                         'categories':records,
                                         'selected_category':category,
                                         })

def change_category(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body.decode('utf-8'))

            if 'items_json_data' in request.session:
                request.session['items_json_data'].update(json_data)
            else:
                request.session['items_json_data'] = json_data

            print(request.session['items_json_data'])

            return JsonResponse({'success': True})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'خطا در تحلیل JSON'})
    else:
        return JsonResponse({'error': 'فقط درخواست‌های POST مورد پذیرش هستند'})

def shoping_cart(request):
    return render(request,'customer/shoping-cart.html',context={})

def table_rigester(request):
    return render(request,'customer/table-rigester.html',context={})

def delete_order(request,del_id):
    del_order = Customer_order.objects.filter(pk = del_id).update(is_deleted=True)
    return render(request,"staff/dashboard.html" , context={"del_order":del_order})
    
def change_status(request,status_id):
    status_list=['Pending','Confirmed','Cooking','Ready Delivery','Deliverd','Checked Out']
    status_order = Customer_order.objects.filter(pk=status_id)
    return render(request,"staff/dashboard.html" , context={"change":status_order,"status_list":status_list})
        
        
