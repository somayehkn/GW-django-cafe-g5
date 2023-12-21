from django.shortcuts import render

# Create your views here.

def shoping_cart(request):
    return render(request,'customer/shoping-cart.html',context={})

def table_rigester(request):
    return render(request,'customer/table-rigester.html',context={})

