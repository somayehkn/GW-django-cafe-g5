from django.shortcuts import render
from .models import Category, Item

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
    category = request.GET.get('cat')
    category = Category.objects.get(name=category)
    category_items = Item.objects.filter(category=category)
    records = Category.objects.all()
    return render(request, 'menu.html', {'category_items':category_items,'categories':records})