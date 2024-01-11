# customer/tests/test_views.py
import json
from django.test import TestCase, Client
from django.urls import reverse
from customer.models import Table, Customer, Category, Item, Customer_order, Order_item

class CustomerViewsTest(TestCase):
    def setUp(self):
        # ایجاد یک مشتری و یک محصول برای استفاده در تست
        self.customer = Customer.objects.create(first_name="John", last_name="Doe", phone_number="123456789")
        self.category = Category.objects.create(name="Food", description="Delicious food")
        self.item = Item.objects.create(name="Burger", category=self.category, unitprice=10.0)

        # ایجاد یک میز برای استفاده در تست
        self.table = Table.objects.create(table_number=1, capacity=4)

    def test_menu_view(self):
        # شبیه‌سازی درخواست GET برای ویو
        response = self.client.get(reverse('menu'))

        # بررسی کد وضعیت HTTP
        self.assertEqual(response.status_code, 200)

        # بررسی وجود داده‌های مدل در صفحه
        self.assertContains(response, self.category.name)
        self.assertContains(response, self.item.name)

    def test_save_items_to_session_view(self):
        # شبیه‌سازی درخواست POST برای ذخیره اطلاعات در سشن
        data = {
            'Burger': {'item_quantity': 2, 'item_total_price': 20.0},
        }
        response = self.client.post(reverse('save-items-to-sesion'), json.dumps(data), content_type='application/json')

        # بررسی کد وضعیت HTTP
        self.assertEqual(response.status_code, 200)

        # بررسی اطلاعات درج شده در سشن
        self.assertEqual(self.client.session['items_json_data'], data)

    def test_register_order_view(self):
        # شبیه‌سازی درخواست POST برای ثبت سفارش
        data = {
            'tableNumber': 1,
        }
        response = self.client.post(reverse('register_order'), json.dumps(data), content_type='application/json')

        # بررسی کد وضعیت HTTP
        self.assertEqual(response.status_code, 200)

        # بررسی ذخیره‌سازی مناسب در دیتابیس
        self.assertEqual(Customer_order.objects.count(), 1)
        self.assertEqual(Order_item.objects.count(), 1)
        self.assertEqual(Order_item.objects.first().count, 2)

    # موارد دیگر تست‌ها (checkout_page و shoping_cart و غیره) می‌توانند به همین شکل افزوده شوند
