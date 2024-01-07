from django.http import HttpResponse
from django.http.response import HttpResponse as HttpResponse
from django.core.files.storage import FileSystemStorage
from django.db.models.functions import TruncHour,ExtractHour
from django.db.models import Sum, Count
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
from typing import Any
from customer.models import Category, Item, Customer_order, Order_item,Table
from .models import User, OTPCODE
from .forms import  Form_Category,UserRegister,VerifyCodeForm,LoginForm
from utils import send_otp_code
from datetime import datetime, timedelta
import shutil
import os
import random
import json

def reports(request):
    # get all orders
    all_orders = Customer_order.objects.filter(is_deleted=False)
    checked_out_orders = Customer_order.objects.filter(is_deleted=False, status='Checked Out')
    other_orders = Customer_order.objects.filter(is_deleted=False).exclude(status='Checked Out')
    
    # income info boxes
    today = timezone.now().date()
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
    first_chart_data = [entry['earnings'] if entry['earnings'] else 0 for entry in daily_earnings]
    
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
    labels = [f"{hour} - {hour + 1}" for hour in range(9, 23)]
    data = [0] * 14

    for order in orders_by_hour:
        data[order['hour'] - 9] = order['order_count']

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
    
    # create pdf file
    table_data = [
        ['Total Income', 'Today Income', 'Today Orders', 'Pending Orders'],
        [f'{total_earnings}', f'{today_earnings}', f'{today_checked_out_orders}', f'{today_other_orders}'],
    ]
    
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
                return redirect(reverse("dashboard"))
            messages.add_message(request,messages.ERROR,f"user {username} was not found!")
    return render(request,'staff/login.html',context={"form":form})

def dashboard(request):
    customer_orders = Customer_order.objects.all()
    
    return render(request,'staff/dashboard.html',context={'customer_orders': customer_orders})
    
def logout(request):
    django_logout(request)
    return redirect(reverse("dashboard")) 

class TestView(View):
    def get(self,request):
        form = Form_Category()
        previous_url = request.META.get('HTTP_REFERER',None)
        return render(request,"staff/add-category.html",{"form":form , 'previous_url':previous_url})

    def post(self,request):
        category_name= request.POST.get("category_name")
        description = request.POST.get("description")


        image = request.FILES.get("category_img")
            
        

        form = Form_Category(data=request.POST,files=request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            fs = FileSystemStorage()
            # save the image on MEDIA_ROOT folder
            file_name = fs.save(image.name, image)
            # get file url with respect to `MEDIA_URL`
            file_url = f"uploads/{image}"
       
            # shutil.copy(file_url, destination_path)
            old_media_url = file_url
    
            
            # انجام عملیات کپی و حذف و بازگرداندن ادرس فایل جدید
            new_media_url = move_and_delete_media_url(old_media_url)
            print(new_media_url)
            instance = form.save(commit=False)
            instance.image = new_media_url 
            instance.save()

        

        #redirect to the previous page using request.META.get('HTTP_REFERER')
        previous_url = request.META.get('HTTP_REFERER',None)
        
        
        return render(request,"staff/add-category.html",{"form":form, 'previous_url':previous_url})

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


