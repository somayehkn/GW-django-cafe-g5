from django.urls import path
from . import views 

urlpatterns = [
    path("shoping-cart",views.shoping_cart,name="shoping-cart"),
    path("table-rigester",views.table_rigester,name="table-rigester"),
    


]