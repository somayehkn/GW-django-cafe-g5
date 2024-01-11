from django.test import TestCase
from django.utils import timezone
from customer.models import Table, Customer, Category, Item, Customer_order, Order_item

class ModelTests(TestCase):
    def test_table_str(self):
        table = Table.objects.create(table_number=1, capacity=4)
        self.assertEqual(str(table), '1')

    def test_customer_str(self):
        customer = Customer.objects.create(phone_number='1234567890')
        self.assertEqual(str(customer), '1234567890')

    def test_category_str(self):
        category = Category.objects.create(name='Test Category', description='Test Description')
        self.assertEqual(str(category), 'Test Category')

    def test_item_str(self):
        category = Category.objects.create(name='Test Category', description='Test Description')
        item = Item.objects.create(name='Test Item', category=category, unitprice=10.0)
        self.assertEqual(str(item), 'Test Item')

    def test_customer_order_save(self):
        table = Table.objects.create(table_number=1, capacity=4)
        customer_order = Customer_order.objects.create(table_number=table, total_price=20.0)
        customer_order.save()
        self.assertIsNotNone(customer_order.timestamp)

    def test_order_item_str(self):
        category = Category.objects.create(name='Test Category', description='Test Description')
        item = Item.objects.create(name='Test Item', category=category, unitprice=10.0)
        table = Table.objects.create(table_number=1, capacity=4)
        customer_order = Customer_order.objects.create(table_number=table, total_price=20.0)
        order_item = Order_item.objects.create(item=item, count=2, customer_order=customer_order)
        self.assertEqual(str(order_item), '2x Test Item')
