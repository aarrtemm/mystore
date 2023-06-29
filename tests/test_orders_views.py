from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from orders.models import Order
from products.models import Basket, Product, Gender

ORDER_LIST = reverse("orders:order-list")
ORDER_DETAIL = "orders:order-detail"
SUCCESS_PAGE = reverse("orders:order-success")
CANCELLED_PAGE = reverse("orders:order-canceled")
ORDER_CREATED = reverse("orders:create-order")


class OrderViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(
            name='Product 1',
            price=10,
            quantity=1,
            gender=Gender.objects.create(name="TestName")
        )
        self.basket = Basket.objects.create(user=self.user, product=self.product)
        self.order = Order.objects.create(
            first_name='John',
            last_name='Doe',
            email='johndoe@example.com',
            address='123 Main St',
            initiator=self.user
        )
        self.order.purchased_goods.add(self.product)
        self.order.save()

    def test_order_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(ORDER_LIST)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_list.html')
        self.assertIn(self.order, response.context['object_list'])
        self.assertEqual(response.context['object_list'].count(), 1)

    def test_order_detail_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse(ORDER_DETAIL, kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_detail.html')
        self.assertEqual(response.context['object'], self.order)

    def test_order_create_view_with_valid_form(self):
        self.client.force_login(self.user)
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "purchased_goods": self.order.purchased_goods,
            "address": "adadasdsd",
            "initiator": self.user.id,
        }
        response = self.client.post(ORDER_CREATED, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, SUCCESS_PAGE)
        self.assertEqual(Order.objects.count(), 2)
        self.assertFalse(Basket.objects.filter(user=self.user).exists())

    def test_order_create_view_with_empty_basket(self):
        self.client.force_login(self.user)
        self.basket.delete()
        response = self.client.post(ORDER_CREATED, data={
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'janedoe@example.com',
            'address': '456 Elm St',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, CANCELLED_PAGE)
        self.assertEqual(Order.objects.count(), 1)
        self.assertFalse(Basket.objects.filter(user=self.user).exists())

    def test_success_template_view(self):
        response = self.client.get(reverse('orders:order-success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/success.html')

    def test_cancel_template_view(self):
        response = self.client.get(reverse('orders:order-canceled'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/canceled.html')
