
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
from customer import views as customer_views
from customer.views import DeleteOrder 
from .views import TestView
urlpatterns = [
    path('add_item', views.add_items, name = 'add_item'),
    path("login/",views.login,name="login"),
    path("dashboard",views.dashboard,name="dashboard"),
    path('add-category/', TestView.as_view(), name = 'add-category'),
    path("register" , views.registerview.as_view(),name = "register"),
    path("verify" , views.UserRegisterVerifyCodeView.as_view(),name="verify_code"),
    path("table",views.table,name="table"),
    path("list_user",views.list_user.as_view(),name="list_user"),
    path("delete_user/<int:pk>/",views.DeleteUser.as_view(),name="delete_user"),
    path("logout",views.logout,name="logout"),
    path("update_order/<order_id>",views.update_order,name="update_order"),
    path("delete_table",customer_views.DeleteOrder.as_view(),name="delete_table"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
