from django.urls import path
from . import views 


path("shoping-cart",views.shoping_cart,name="shoping-cart"),
path("table-rigester",views.table_rigester,name="table-rigester"),