from typing import Any
from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from customer.models import Category, Item
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login as django_login,logout as django_logout
from django.contrib import messages
from django.urls import reverse
from .models import User
from django.views import View
import random
from .forms import UserRegister,VerifyCodeForm,LoginForm
from utils import send_otp_code
from .models import OTPCODE
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

def is_cashier(user):
    return user.is_admin

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
                return redirect(reverse("index"))
            messages.add_message(request,messages.ERROR,f"user {username} was not found!")
    return render(request,'staff/login.html',context={"form":form})


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


def index(request):
    return render(request,'staff/index.html',context={})


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
    success_url = reverse_lazy("index")
    