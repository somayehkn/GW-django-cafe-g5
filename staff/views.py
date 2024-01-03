
from django.shortcuts import render
# from .models import Order
from django.shortcuts import get_object_or_404
from customer.models import Customer_order, Item, Table, Order_item

# def dashboard(request):
#     customer_orders= Customer_order.objects.filter(is_delete=False)
#     orders = {}
#     for order in customer_orders:
#         orders[order]= Order_item.objects.filter(Customer_order=order)
#     return render(request,'staff/dashboard.html',context={'customer_orders': customer_orders})

def order_detail(request, order_id):
    order = get_object_or_404(Customer_order, id=order_id)
    order_items = Order_item.objects.filter(customer_order=order)
    return render(request, 'staff/order_detail.html', {'order': order, 'order_items': order_items}) 

def order_list(request):
    orders_status = Customer_order.objects.all().order_by('status')
    return render(request,'staff\status.html', {'orders_status': orders_status })


    
def order_list_date(request):
    timestamp = Customer_order.objects.all().order_by('timestamp')
    print(timestamp)
    return render(request,'staff\date.html', { 'timestamp':timestamp})



def order_list_filter_status(request):
    orders = []
    
    status = request.GET.get('status', '')
    print(status)
    
    if status:
      orders = Customer_order.objects.filter(status= status)
      print(orders)
     
    context = {'orders': orders }
    return render(request, 'staff/filter-status.html', context)




def order_list_filter_table_number(request):
    orders = []

    table_number = request.GET.get('table_number', '')
    print(table_number)

    if table_number:
        orders = Customer_order.objects.filter(table_number = table_number)
        print(orders)

    context = {'orders': orders}
    return render(request, 'staff/filter-table.html', context)



    # def order_list_filter_date(request):
#     orders = [] 
#     selected_date = request.GET.get('date', '')
#     print(selected_date)

#     if selected_date:
      
#         orders = Order.objects.filter(order_date=selected_date)
#         print(orders)
    
#     context = {'orders': orders}
#     return render(request, 'staff/filter-date.html', context)