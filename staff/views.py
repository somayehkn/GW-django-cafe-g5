from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from customer.models import Category, Item, Customer_order, Order_item,Table
import shutil
from typing import Any
from django.http.response import HttpResponse as HttpResponse
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate,login as django_login,logout as django_logout
from django.contrib import messages
from django.urls import reverse
from django.views import View
from .forms import  Form_Category,UserRegister,VerifyCodeForm,LoginForm,order_table
import os
from .models import User
import random
from utils import send_otp_code
from .models import OTPCODE
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
def is_cashier(user):
    return user.is_admin

def reports(request):
    earning_monthly = earning_annual = today_orders = pending_orders = 0
    sell_in_month_perday = {}
    return render(request,'staff/report.html',context={})


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

@login_required
def dashboard(request):
    customer_orders = Customer_order.objects.all()
    
    return render(request,'staff/dashboard.html',context={'customer_orders': customer_orders})

@login_required    
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
        list_roll=["seff","cashier","waiter"]
        return render(request,'staff/register.html',{'form':form,"list_roll":list_roll})
    
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
def order_list(request):
    orders_status = Customer_order.objects.all().order_by('status')
    return render(request,'staff\status.html', {'orders_status': orders_status })


@login_required    
def order_list_date(request):
    timestamp = Customer_order.objects.all().order_by('timestamp')
    print(timestamp)
    return render(request,'staff\date.html', { 'timestamp':timestamp})


@login_required
def order_list_filter_status(request):
    orders = []
    
    status = request.GET.get('status', '')
    print(status)
    
    if status:
      orders = Customer_order.objects.filter(status= status)
      print(orders)
     
    context = {'orders': orders }
    return render(request, 'staff/filter-status.html', context)



@login_required
def order_list_filter_table_number(request):
    orders = []

    table_number = request.GET.get('table_number', '')
    print(table_number)

    if table_number:
        orders = Customer_order.objects.filter(table_number = table_number)
        print(orders)

    context = {'orders': orders}
    return render(request, 'staff/filter-table.html', context)

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
def update_order(request,order_id):
    order=Customer_order.objects.get(pk=order_id)
    form=order_table(request.POST or None , instance=order)
    if form.is_valid():
        form.save()
        return redirect(reverse("dashboard"))
    return render(request,"staff/update_order.html",context={"order":order,"form":form})


def delete_order(request,del_id):
    del_order = Customer_order.objects.filter(pk = del_id).update(is_deleted=True)
    render(request,"staff/dashboard.html",context={"del_order":del_order})
    return redirect(reverse("dashboard"))

def trash(request):
    customer_orders = Customer_order.objects.filter(is_deleted = True)
    return render(request,'staff/trash.html',context={"customer_orders":customer_orders})

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