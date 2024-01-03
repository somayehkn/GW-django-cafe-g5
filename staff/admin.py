from django.contrib import admin
from .models import Staff
from customer.models import Customer_order,Table, Order_item, Item, Category

admin.site.register(Staff)
# admin.site.register(Order)
admin.site.register(Customer_order)
admin.site.register(Table)
admin.site.register(Order_item)
admin.site.register(Item)
admin.site.register(Category)


# Register your models here.
