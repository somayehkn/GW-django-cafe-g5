# staff/tests/test_views.py
from django.test import TestCase, Client
from django.urls import reverse
from staff.models import Table, Customer_order, Order_item, Category, Item

class StaffViewsTest(TestCase):
    def setUp(self):
        # Create necessary data for testing
        self.table = Table.objects.create(table_number=1, capacity=4)
        self.category = Category.objects.create(name="Food", description="Delicious food")
        self.item = Item.objects.create(name="Burger", category=self.category, unitprice=10.0)
        self.order = Customer_order.objects.create(table_number=self.table, total_price=20.0)

    def test_add_items_view(self):
        # Simulate a POST request to add items
        data = {'item_name': 'Burger', 'item_quantity': 2}
        response = self.client.post(reverse('staff:add_item'), data)

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check if the items are added to the order
        order_items = Order_item.objects.filter(customer_order=self.order)
        self.assertEqual(order_items.count(), 1)
        self.assertEqual(order_items.first().item, self.item)
        self.assertEqual(order_items.first().count, 2)

    def test_order_list_date_view(self):
        # Simulate a GET request to view orders by date
        response = self.client.get(reverse('staff:date'))

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # You can add more assertions related to the specific behavior of the view

    def test_order_list_filter_status_view(self):
        # Simulate a GET request to view orders filtered by status
        response = self.client.get(reverse('staff:filter-status'))

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # You can add more assertions related to the specific behavior of the view

    def test_order_list_filter_table_number_view(self):
        # Simulate a GET request to view orders filtered by table number
        response = self.client.get(reverse('staff:filter-table'))

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # You can add more assertions related to the specific behavior of the view

    def test_order_detail_view(self):
        # Simulate a GET request to view order details
        response = self.client.get(reverse('staff:order_detail', args=[self.order.id]))

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # You can add more assertions related to the specific behavior of the view
