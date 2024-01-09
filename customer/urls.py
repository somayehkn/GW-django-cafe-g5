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
    
    path('', views.home, name='home'),
    path('categories/', views.categories, name='categories'),
    path('menu/<str:foo>/', views.menu, name='menu'),
    path('save-menu-items-to-sesion/', views.save_menu_items_to_session, name='save_menu_items_to_session'),
    path('save-cart-items-to-sesion/', views.save_cart_items_to_session, name='save_cart_items_to_session'),
    path("shoping-cart/",views.shoping_cart, name="shoping-cart"),
    path("table-rigester/",views.table_rigester, name="table-rigester"),
    path('checkout-page/', views.checkout_page, name='checkout-page'),
    path('register-order/', views.register_order, name='register_order'),

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



