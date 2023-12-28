"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings  
from django.conf.urls.static import static  
from . import views
urlpatterns = [
    path('add_item', views.add_items, name = 'add_item'),
    path("",views.login,name="login"),
    path("register" , views.registerview.as_view(),name = "register"),
    path("verify" , views.UserRegisterVerifyCodeView.as_view(),name="verify_code"),
    path("index",views.index,name="index"),
    path("table",views.table,name="table"),
    path("list_user",views.list_user.as_view(),name="list_user"),
    path("delete_user/<int:pk>/",views.DeleteUser.as_view(),name="delete_user"),
    path("logout",views.logout,name="logout")
    

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
