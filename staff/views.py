from django.core.files.storage import FileSystemStorage
from customer.models import Category, Item, Customer_order, Order_item
import shutil
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate,login as django_login,logout as django_logout
from django.contrib import messages
from django.urls import reverse
from django.views import View
from .forms import  Form_Category
import os

# Create your views here.
@requires_csrf_token
def add_items(request):
    if request.method == 'POST':
        image = request.FILES['file_input']
        fs = FileSystemStorage()

        # save the image on MEDIA_ROOT folder
        file_name = fs.save(image.name, image)

        # get file url with respect to `MEDIA_URL`
        file_url = f"uploads/{image}"
        # shutil.copy(file_url, destination_path)
        
        
        item_name = request.POST.get('item_name')
        item_price = request.POST.get('item_price')
        item_info = request.POST.get('item_info')
        image = file_url
        category = request.POST.get('selected_category')
        category = Category.objects.get(name=category)
        category_id = category.id
        
        # ساخت یک شیء جدید از مدل Item
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
        form = AuthenticationForm()
    elif request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
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
    return redirect(reverse("index")) 

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

