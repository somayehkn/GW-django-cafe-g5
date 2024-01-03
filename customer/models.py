from django.db import models

# Create your models here.
class Table(models.Model):
    table_number = models.IntegerField()
    capacity = models.IntegerField()

    def __str__(self) -> str:
        return str(self.table_number)


class Customer(models.Model):
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    phone_number = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.phone_number


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='cat_images/', null=True)
    is_exist = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name
    
class Item(models.Model):
    name = models.CharField(max_length=20)
    category: Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    unitprice = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='item_images/', null=True)
    is_exist = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name
    
class Customer_order(models.Model):
    STATUS_CHOICES = [
        ('Deliverd','Deliverd'),
        ('Confirmed', 'Confirmed'),
        ('Cooking', 'Cooking'),
        ('Ready Delivery', 'Ready Delivery') 
     ]
    timestamp = models.DateTimeField()
    description = models.TextField(null=True)
    table_number = models.ForeignKey(Table, null=True, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)



class Order_item(models.Model):
    item: Item = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    customer_order: Customer_order = models.ForeignKey(Customer_order, on_delete=models.CASCADE)


