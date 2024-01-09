
from django.urls import path
from django.conf import settings  
from django.conf.urls.static import static  
from . import views
from .views import TestView, order_list_date, order_list_filter_status,  order_list_filter_table_number, order_list, order_detail


urlpatterns = [
    path('add_item', views.add_items, name = 'add_item'),
    path("login/",views.login,name="login"),
    path("dashboard",views.dashboard_deliverd,name="dashboard"),
    path('add-category/', TestView.as_view(), name = 'add-category'),
    path("register" , views.registerview.as_view(),name = "register"),
    path("verify" , views.UserRegisterVerifyCodeView.as_view(),name="verify_code"),
    path("table",views.table,name="table"),
    path("list_user",views.list_user.as_view(),name="list_user"),
    path("reports",views.reports,name="reports"),
    path("delete_user/<int:pk>/",views.DeleteUser.as_view(),name="delete_user"),
    path("logout",views.logout,name="logout"),
    path('status/', order_list, name='status'),
    path('date/', order_list_date, name='date'),
    path('filter-status/', order_list_filter_status, name='filter-status'),
    path('filter-table/', order_list_filter_table_number, name='filter-table'),
    path('order_detail/<int:order_id>/', order_detail, name='order_detail'),
    path("update_order/<order_id>",views.update_order,name="update_order"),
    path("delete_table/<del_id>",views.delete_order,name="delete_table"),
    path("trash",views.trash,name="trash"),
    path("checked_out",views.checked_out,name="checked_out"),
    path("back_delete/<del_id>",views.back_delete,name="back_delete"),
    path("update_model/<item_id>",views.update_model,name="update_model"),

]

    



