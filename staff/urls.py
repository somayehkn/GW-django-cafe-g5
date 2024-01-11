
from django.urls import path
from django.conf import settings  
from django.conf.urls.static import static  
from . import views
from .views import  order_list_date, order_list_filter_status,  order_list_filter_table_number, order_detail, add_items

app_name = 'staff'
urlpatterns = [
    path('add_item', views.add_items, name = 'add_item'),
    path("login/",views.login,name="login"),
    path("dashboard",views.dashboard,name="dashboard"),
    path('add-category/', views.add_category, name = 'add-category'),
    path("register" , views.registerview.as_view(),name = "register"),
    path("verify" , views.UserRegisterVerifyCodeView.as_view(),name="verify_code"),
    path("table",views.table,name="table"),
    path("list_user",views.list_user.as_view(),name="list_user"),
    path("reports",views.reports,name="reports"),
    path("delete_user/<int:pk>/",views.DeleteUser.as_view(),name="delete_user"),
    path("logout",views.logout,name="logout"),
    path('date/', views.order_list_date, name='date'),
    path('filter-status/', views.order_list_filter_status, name='filter-status'),
    path('filter-table/', views.order_list_filter_table_number, name='filter-table'),
    path('order_detail/<int:order_id>/', order_detail, name='order_detail'),
]

    



