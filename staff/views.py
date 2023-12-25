from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from customer.models import Category, Item
import shutil
from django.views.decorators.csrf import requires_csrf_token
from django.views import View
from .forms import  Form_Category


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
        
    
import shutil
import os

def move_and_delete_media_url(old_file_path):
    img_name = (old_file_path.split("/"))[-1]
    new_file_path = f"static/assets_home_page/img/{img_name}"
   
    # کپی کردن فایل به مسیر جدید
    shutil.copy(old_file_path, new_file_path)
    
    # حذف فایل از مسیر قبلی در مدیا یو ار ال
    os.remove(old_file_path)
    new_file_path = f"assets_home_page/img/{img_name}"
    return new_file_path # بازگرداندن ادرس فایل جدید
