from django.db import models
from django.utils import timezone



# Create your models here.


class Staff(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20,null=True)
    phone_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    
# class Order(models.Model):
#     STATUS_CHOICES = [
#         ('Deliverd','Deliverd'),
#         ('Confirmed', 'Confirmed'),
#         ('Cooking', 'Cooking'),
#         ('Ready Delivery', 'Ready Delivery') 
#     ]
#     table_number = models.IntegerField()
#     order_date = models.DateTimeField(default= timezone.now)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    
#     def __str__(self):
#         return f"{self.table_number} - {self.order_date}"