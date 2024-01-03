

from django.urls import path
from . import views
from django.conf.urls.static import static  
from .views import order_list, order_list_date, order_list_filter_status, order_list_filter_table_number, order_detail





urlpatterns = [
    path('status/', order_list, name='status'),
    path('date/', order_list_date, name='date'),
    path('filter-status/', order_list_filter_status, name='filter-status'),
    # path('filter-date/', order_list_filter_date, name='filter-date'),
    path('filter-table/', order_list_filter_table_number, name='filter-table'),
    path('d', order_list_filter_table_number, name='filter-table'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),

]
