from django.http import HttpResponse,JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.core.files.storage import FileSystemStorage
from django.db.models.functions import TruncHour,ExtractHour
from django.db.models import Sum, Count
from .models import OTPCODE,User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate,login as django_login,logout as django_logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.decorators.csrf import requires_csrf_token
from django.views import View
from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from utils import send_otp_code
from .forms import  UserRegister,VerifyCodeForm,LoginForm,order_table
from customer.models import *
import shutil
import os
import random
import json
from django import template

register = template.Library()

@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    return qty * unit_price

@login_required
def dashboard(request):
    if request.method == 'POST':
        customer_order_id = request.POST.get('customer_order_id')
        customer_order_status = request.POST.get('customer_order_status')
        
        Customer_order.objects.filter(pk=customer_order_id).update(status=customer_order_status)
        # customer_order = get_object_or_404(Customer_order, pk=customer_order_id).update(status = customer_order_status)
        # customer_order.status = customer_order_status
        # customer_order.save()
    customer_orders_confirmed = Customer_order.objects.filter(is_deleted = False,status = "Confirmed")
    customer_orders_cooking = Customer_order.objects.filter(is_deleted = False,status = "Cooking")
    customer_orders_ready_delivery = Customer_order.objects.filter(is_deleted = False,status = "Ready Delivery")
    customer_orders_deliverd = Customer_order.objects.filter(is_deleted = False,status = "Deliverd")
    return render(request,'staff/dashboard.html',context={'customer_orders_confirmed': customer_orders_confirmed,'customer_orders_cooking': customer_orders_cooking,'customer_orders_deleverd': customer_orders_deliverd,'customer_orders_ready_delivery': customer_orders_ready_delivery})



@login_required
def reports(request):
    # get all orders
    all_orders = Customer_order.objects.filter(is_deleted=False)
    checked_out_orders = Customer_order.objects.filter(is_deleted=False, status='Checked Out')
    other_orders = Customer_order.objects.filter(is_deleted=False).exclude(status='Checked Out')
    
    # income info boxes
    today = timezone.now().date()
    print (today)
    today_checked_out_orders = total_earnings = today_earnings = today_other_orders = 0
    for order in checked_out_orders:
        total_earnings += order.total_price
        if today == order.timestamp.date():
            today_checked_out_orders += 1
            today_earnings += order.total_price
    for order in other_orders:
        if today == order.timestamp.date():
            today_other_orders += 1
            
    # first chart (monthly sales)
    one_month_ago = timezone.now() - timezone.timedelta(days=30)
    orders = Customer_order.objects.filter(timestamp__gte=one_month_ago, is_deleted=False)
    daily_earnings = orders.filter(status='Checked Out').values('timestamp__date').annotate(earnings=Sum('total_price'))
    first_chart_labels = [entry['timestamp__date'].strftime('%d') for entry in daily_earnings]
    first_chart_data_fake = [entry['earnings'] if entry['earnings'] else 0 for entry in daily_earnings]
    first_chart_data = []
    for item in first_chart_data_fake:
        first_chart_data.append(float(item))
    
    
    
    # second chart (top sales products)
    popular_items = Order_item.objects.values('item__name').annotate(total_orders=Count('item')).order_by('-total_orders')[:5]
    second_chart_labels = [item['item__name'] for item in popular_items]
    second_chart_data = [item['total_orders'] for item in popular_items]
    
    # third chart (product sales percentages)
    all_items = Item.objects.filter(is_exist=True)
    total_sales = Order_item.objects.count()
    items_sales_percentage = []
    for item in all_items:
        item_sales_count = Order_item.objects.filter(item=item).count()
        percentage = (item_sales_count / total_sales) * 100 if total_sales > 0 else 0
        items_sales_percentage.append({'name': item.name, 'percentage': int(percentage)})
    
    # fourth chart (work peek hours)
    orders_by_hour = Customer_order.objects.filter(is_deleted=False).annotate(hour=ExtractHour('timestamp')).values('hour').annotate(order_count=Count('id')).order_by('hour')
    data_dict = {hour: 0 for hour in range(9, 23)}

    for order in orders_by_hour:
        data_dict[order['hour']] = order['order_count']

    labels = [f"{hour} - {hour + 1}" for hour in range(9, 23)]
    data = list(data_dict.values())
    # labels = [f"{hour} - {hour + 1}" for hour in range(9, 23)]
    # data = [0] * 14

    # for order in orders_by_hour:
    #     print(order['hour'] - 9)
    #     data[order['hour'] - 9] = order['order_count']

    chart_data = {
        "type": "bar",
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "label": "Order Counts",
                    "backgroundColor": "#4e73df",
                    "borderColor": "#4e73df",
                    "data": data
                }
            ]
        },
        "options": {
            "maintainAspectRatio": True,
            "legend": {"display": False},
            "title": {"fontStyle": "bold"}
        }
    }
    peek_hour_chart = json.dumps(chart_data)
    return render(request,'staff/report.html',
                  context={
                      'total_earnings': total_earnings,
                      'today_earnings': today_earnings, 
                      'today_checked_out_orders': today_checked_out_orders,
                      'today_other_orders':today_other_orders,
                      'monthly_chart_labels': first_chart_labels, 
                      'monthly_chart_data': first_chart_data, 
                      'second_chart_labels': second_chart_labels,
                      'second_chart_labels0':second_chart_labels[0],
                      'second_chart_labels1':second_chart_labels[1],
                      'second_chart_labels2':second_chart_labels[2],
                      'second_chart_labels3':second_chart_labels[3],
                      'second_chart_labels4':second_chart_labels[4],
                      'second_chart_data': second_chart_data, 
                      'items_sales_percentage': items_sales_percentage,
                      'peek_hour_chart': peek_hour_chart,
                      }
                  )

def is_cashier(user):
    return user.is_admin

# Create your views here.
@requires_csrf_token
def add_items(request):
    if request.method == 'POST':
        image = request.FILES['file_input']
        fs = FileSystemStorage()
        file_name = fs.save(image.name, image)
        old_media_url = f"uploads/{image}"
        new_file_path = f"static/assets_menu_page/img/{image}"
        shutil.copy(old_media_url, new_file_path)
        os.remove(old_media_url)
        new_file_path = f"assets_menu_page/img/{image}"
        
        item_name = request.POST.get('item_name')
        item_price = request.POST.get('item_price')
        item_info = request.POST.get('item_info')
        image = new_file_path
        category = request.POST.get('selected_category')
        print(category)
        category = Category.objects.get(name=category)
        category_id = category.id
        new_item = Item(
            name=item_name,
            unitprice=item_price,
            description=item_info,
            category_id=category_id,
            image = image
        )
        
        new_item.save()
    context = Category.objects.all()
    return render(request, 'staff/add_item.html',{'categories':context})

@requires_csrf_token
def add_category(request):
    if request.method == 'POST':
        image = request.FILES['file_input']
        fs = FileSystemStorage()
        file_name = fs.save(image.name, image)
        old_media_url = f"uploads/{image}"
        new_file_path = f"static/assets_menu_page/img/{image}"
        shutil.copy(old_media_url, new_file_path)
        os.remove(old_media_url)
        new_file_path = f"assets_menu_page/img/{image}"
        
        category_name = request.POST.get('category_name')
        category_info = request.POST.get('category_info')
        image = new_file_path
        
        new_category = Category(
            name=category_name,
            description=category_info,
            image = image
        )
        
        new_category.save()
    
    return render(request, 'staff/add-category.html',{})







# create view for login
def login(request):
    if request.method == "GET":
        form = LoginForm()
    elif request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["phone"]
            password = form.cleaned_data["password"]  
            user = authenticate(request,username=username,password=password)
            if user is not None:
                django_login(request,user)
                messages.add_message(request,messages.SUCCESS,f"welcome{username}")
                return redirect("dashboard")
            messages.add_message(request,messages.ERROR,f"user {username} was not found!")
    return render(request,'staff/login.html',context={"form":form})

   

def move_and_delete_media_url(old_file_path):
    img_name = (old_file_path.split("/"))[-1]
    new_file_path = f"static/assets_home_page/img/{img_name}"
   
    # کپی کردن فایل به مسیر جدید
    shutil.copy(old_file_path, new_file_path)
    
    # حذف فایل از مسیر قبلی در مدیا یو ار ال
    os.remove(old_file_path)
    new_file_path = f"assets_home_page/img/{img_name}"
    return new_file_path # بازگرداندن ادرس فایل جدید

@login_required    
def logout(request):
    django_logout(request)
    return redirect(reverse("login")) 

class registerview(View):
    form_class = UserRegister
    
    @method_decorator(user_passes_test(is_cashier), name='dispatch')
    def get(self,request):
        form = self.form_class
        return render(request,'staff/register.html',{'form':form})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
             random_code = random.randint(1000,9999)
             send_otp_code(form.cleaned_data['phone'],random_code)
             OTPCODE.objects.create(phone_number=form.cleaned_data['phone'] , code =random_code)
             request.session['user_registration_info'] ={
                'roll':form.cleaned_data['roll'],
                'phone_number':form.cleaned_data['phone'],
                'email':form.cleaned_data['email'],
                'full_name':form.cleaned_data['full_name'],
                'password':form.cleaned_data['password']
             } 
             messages.success(request,'we sent you a code' , 'success')
             return redirect(reverse('verify_code'))
        return redirect(reverse('login'))
    
  
class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm
    def get(self,request):
        form = self.form_class
        return render(request , 'staff/verify.html' , {'form':form})
    
    def post(self,request):
        user_session = request.session['user_registration_info']
        code_instance = OTPCODE.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data 
            if cd['code'] == code_instance.code:
                User.objects.create_user(user_session['phone_number'],user_session['email'],user_session['full_name'],user_session['password'],user_session['roll'])
    
                code_instance.delete()
                messages.success(request,'you registerd','success')
                return redirect(reverse("register"))

            else:
                messages.error(request,'THis code is wrong','danger')
                return redirect(reverse("verify_code"))
            
        return redirect(reverse("register"))


def table(request):
    return render(request,'staff/table.html',context={})

        
class list_user(View):
    @method_decorator(user_passes_test(is_cashier), name='dispatch')
    def get(self,request):
        user_list=User.objects.all()
        return render(request,"staff/list_user.html",context={'User':user_list})

class DeleteUser(SuccessMessageMixin,DeleteView):
    model = User
    template_name = "staff/remove.html"
    success_message = 'User as been deleted'
    success_url = reverse_lazy("dashboard")


@login_required    
def order_detail(request, order_id):
    order = get_object_or_404(Customer_order, id=order_id)
    order_items = Order_item.objects.filter(customer_order=order)
    return render(request, 'staff/order_detail.html', {'order': order, 'order_items': order_items}) 
    
@login_required
def order_list_date(request):
    timestamp = Customer_order.objects.all().exclude(is_deleted=True).order_by('timestamp')
    return render(request,'staff/date.html', { 'timestamp':timestamp})

@login_required
def order_list_filter_status(request):
    orders = []
    
    status = request.GET.get('status', '')
    
    if status:
        orders = Customer_order.objects.filter(status= status).exclude(is_deleted=True)
    else:
        orders = Customer_order.objects.all().exclude(is_deleted=True).order_by('status','timestamp')
     
    context = {'orders': orders}
   
    return render(request, 'staff/filter-status.html', context)

@login_required
def order_list_filter_table_number(request):
    orders = []

    table_number = request.GET.get('table_number', '')

    if table_number:
        orders = Customer_order.objects.filter(table_number = table_number).exclude(is_deleted=True)
    else:
        orders = Customer_order.objects.all().exclude(is_deleted=True).order_by('table_number','timestamp')

    context = {'orders': orders}
    return render(request, 'staff/filter-table.html', context)


def update_model(request, item_id):
    if request.method == 'POST' and request.is_ajax():
        selected_status = request.POST.get('selectedStatus')  # اطلاعات ارسالی از جاوااسکریپت
       
        # بروزرسانی مدل مورد نظر
        try:
            your_item = Customer_order.objects.get(id=item_id)
            your_item.status = selected_status
            your_item.save()
            return JsonResponse({'success': True})
        except Customer_order.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'آیتم مورد نظر یافت نشد'}, status=404)

    return JsonResponse({'success': False, 'error': 'درخواست نامعتبر'}, status=400)

@login_required
def update_order(request,order_id):
    order=Customer_order.objects.get(pk=order_id)
    form=order_table(request.POST or None , instance=order)
    if form.is_valid():
        form.save()
        return redirect(reverse("dashboard"))
    return render(request,"staff/update_order.html",context={"order":order,"form":form})

@login_required
def delete_order(request,del_id):
    del_order = Customer_order.objects.filter(pk = del_id).update(is_deleted=True)
    render(request,"staff/dashboard.html",context={"del_order":del_order})
    return redirect(reverse("dashboard"))

@login_required
def trash(request):
    customer_orders = Customer_order.objects.filter(is_deleted = True)
    return render(request,'staff/trash.html',context={"customer_orders":customer_orders})

@login_required
def checked_out(request):
    checked_out_orders = Customer_order.objects.filter(status = "Checked Out")
    return render(request,'staff/checked_out.html',context={"checked_out_orders":checked_out_orders})
    
def back_delete(request,del_id):
    del_order = Customer_order.objects.filter(pk = del_id).update(is_deleted=False)
    render(request,"staff/trash.html",context={"del_order":del_order})
    return redirect(reverse("trash"))

def roll_list(request):
    list_roll=["seff","cashier","waiter"]
    return render(request,"staff/register.html",context={"list_roll":list_roll})


