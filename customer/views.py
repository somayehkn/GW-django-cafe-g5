from django.shortcuts import render
from .models import Category, Item

# Create your views here.
def checkout_page (request):
       
    return render(request, 'customer/checkout_page.html',context ={} )

