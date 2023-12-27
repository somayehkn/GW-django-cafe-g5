from django.shortcuts import render
from .models import Category, Item
import json
from django.http import JsonResponse

# Create your views here.

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
    if  request.session['items_json_data']:
        data = request.session['items_json_data']
    category = request.GET.get('cat')
    category = Category.objects.get(name=category)
    category_items = Item.objects.filter(category=category)
    records = Category.objects.all()
    return render(request, 'menu.html', {'category_items':category_items,
                                         'categories':records,
                                         'selected_category':category,
                                         'data': data})

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


