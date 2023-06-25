from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from products.models import Product, Gender
from orders.models import Order


class OrderModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        gender = Gender.objects.create(name="TestGender")
        self.product1 = Product.objects.create(
            name="Product 1", price=10, quantity=1, gender=gender
        )
        self.product2 = Product.objects.create(
            name="Product 2", price=15, quantity=1, gender=gender
        )
        self.order = Order.objects.create(
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            address="123 Main St",
            initiator=self.user,
        )
        self.order.purchased_goods.add(self.product1, self.product2)

    def test_calculate_total_sum(self):
        expected_total = Decimal(25)  # Expected total sum: 10 + 15 = 25
        actual_total = self.order.calculate_total_sum()
        self.assertEqual(actual_total, expected_total)

    def test_order_str_representation(self):
        expected_str = f"Order #{self.order.id}. John Doe"
        actual_str = str(self.order)
        self.assertEqual(actual_str, expected_str)
