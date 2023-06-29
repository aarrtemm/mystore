from _decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from products.models import Basket, Product, Gender, ProductCategory
from users.forms import SingUpForm, UserLoginForm, UserProfileForm

REGISTRATION_URL = reverse("users:register")
LOGIN_URL = reverse("users:login")
LOGOUT_URL = reverse("users:logout")
PROFILE_URL = reverse("users:profile")
INDEX_URL = reverse("products:index")


class RegistrationViewTest(TestCase):
    def setUp(self):
        self.url = REGISTRATION_URL

    def test_registration_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/registration.html')
        self.assertContains(response, '<form')
        self.assertIsInstance(response.context['form'], SingUpForm)

    def test_registration_view_post_valid_form(self):
        data = {
            "first_name": "Iven",
            "last_name": "Birth",
            "email": "qwer@gmail.com",
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        response = self.client.post(self.url, data=data)
        self.assertRedirects(response, LOGIN_URL)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(get_user_model().objects.first().username, 'testuser')

    def test_registration_view_post_invalid_form(self):
        data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'mismatchedpassword',
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/registration.html')
        self.assertContains(response, '<form')
        self.assertIsInstance(response.context['form'], SingUpForm)
        self.assertContains(response, 'password2')


class UserLoginViewTest(TestCase):
    def setUp(self):
        self.url = LOGIN_URL
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpassword'
        )

    def test_user_login_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, '<form')
        self.assertIsInstance(response.context['form'], UserLoginForm)

    def test_user_login_view_post_valid_credentials(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        response = self.client.post(self.url, data=data)
        self.assertRedirects(response, INDEX_URL)

    def test_user_login_view_post_invalid_credentials(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, '<form')
        self.assertIsInstance(response.context['form'], UserLoginForm)
        self.assertContains(response, 'Please enter a correct username and password')


class UserLogoutViewTest(TestCase):
    def setUp(self):
        self.url = LOGOUT_URL

    def test_user_logout_view(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, LOGIN_URL)


class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass",
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
        )
        self.url = PROFILE_URL
        category = ProductCategory.objects.create(name="testcategory")
        product = Product.objects.create(
            name='testproduct',
            price=Decimal('22.22'),
            quantity=2,
            gender=Gender.objects.create(name="gendertest"),
        )
        product.categories.set([category.id])
        product.save()
        self.basket = Basket.objects.create(
            user=self.user,
            product=product,
            quantity=1
        )

    def test_profile_view_authenticated_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/profile.html')
        self.assertContains(response, '<form')
        self.assertIsInstance(response.context['form'], UserProfileForm)
        self.assertQuerysetEqual(
            response.context['baskets'],
            [repr(self.basket)],
            transform=lambda x: repr(x)
        )

    def test_profile_view_no_authenticated_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"{LOGIN_URL}?next={self.url}")