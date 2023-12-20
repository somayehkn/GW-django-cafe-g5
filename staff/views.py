
from django.core.files.storage import FileSystemStorage
from customer.models import Category, Item
import shutil
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate,login as django_login,logout as django_logout
from django.contrib import messages
from django.urls import reverse

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
    return render(request,'login.html',context={"form":form})

def dashboard(request):
    return render(request,'dashboard.html',context={})
    
def logout(request):
    django_logout(request)
    return redirect(reverse("index")) 