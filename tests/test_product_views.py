from decimal import Decimal
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from products.models import (
    Product,
    ProductCategory,
    Gender,
    Basket
)


INDEX = reverse('products:index')
PRODUCT_LIST = reverse('products:products')
PRODUCT_DETAIL = "products:product_detail",
PRODUCT_CREATE = reverse('products:product_create')
PRODUCT_UPDATE = "products:product_update"
PRODUCT_DELETE = "products:product_delete"
IMAGE_FILE = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'media/products_images/images.jpg',
            content_type='image/jpeg'
        )


class IndexViewTest(TestCase):
    def test_index_view(self):
        response = self.client.get(INDEX)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/index.html')


class ProductListViewTest(TestCase):
    def setUp(self):
        ProductCategory.objects.create(name='TestCategory')
        gender = Gender.objects.create(name='TestGender')

        Product.objects.create(
            name='TestProduct',
            price=10,
            quantity=5,
            gender=gender,
            image=IMAGE_FILE
        )
        self.url = PRODUCT_LIST

    def test_product_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertQuerysetEqual(
            response.context['products'],
            ['TestProduct'],
            transform=lambda x: x.name
        )
        self.assertQuerysetEqual(
            response.context['categories'],
            ['TestCategory'],
            transform=lambda x: x.name
        )
        self.assertQuerysetEqual(
            response.context['genders'],
            ['TestGender'],
            transform=lambda x: x.name
        )


class ProductDetailViewTest(TestCase):
    def setUp(self):
        gender = Gender.objects.create(name='TestGender')

        self.product = Product.objects.create(
            name='TestProduct',
            price=10,
            quantity=5,
            gender=gender,
            image=IMAGE_FILE
        )
        self.url = reverse("products:product_detail", args=[self.product.id])

    def test_product_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        self.assertEqual(response.context['product'], self.product)
        self.assertIn('form', response.context)
        self.assertIn('quantity', response.context)


class ProductCreateViewTest(TestCase):
    def setUp(self):
        category = ProductCategory.objects.create(name="TestCategory")
        gender = Gender.objects.create(name="TestGender")
        self.url = PRODUCT_CREATE
        self.valid_data = {
            "name": "TestProduct",
            "price": Decimal("22.22"),
            "quantity": 11,
            "categories": [category.id],
            "gender": gender.id,
        }
        self.invalid_data = {
            "name": "Test Product",
            "price": -1,
            "quantity": 2,
            "image": IMAGE_FILE,
            "gender": 1,
            "categories": category
        }

    def test_create_product_success(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), 1)

    def test_create_product_invalid_data(self):
        response = self.client.post(self.url, data=self.invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Product.objects.filter(name="Test Product").exists())
        self.assertFormError(response, "form", "price", [])


class ProductUpdateViewTest(TestCase):
    def setUp(self):
        gender = Gender.objects.create(name='TestGender')
        category = ProductCategory.objects.create(name="TestCategory")
        self.product = Product.objects.create(
            name='TestProduct',
            price=10,
            quantity=5,
            gender=gender,
            image=IMAGE_FILE
        )
        self.url = reverse(PRODUCT_UPDATE, args=[self.product.id])
        self.data = {
            'name': 'UpdatedProduct',
            'price': Decimal("22.22"),
            'quantity': 3,
            'gender': gender.id,
            "categories": [category.id]
        }

    def test_product_update_view(self):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('products:products'))
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'UpdatedProduct')
        self.assertEqual(self.product.price, Decimal("22.22"))
        self.assertEqual(self.product.quantity, 3)


class ProductDeleteViewTest(TestCase):
    def setUp(self):
        gender = Gender.objects.create(name='TestGender')
        self.product = Product.objects.create(name='TestProduct', price=10, quantity=5, gender=gender)
        self.url = reverse(PRODUCT_DELETE, args=[self.product.id])

    def test_product_delete_view(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('products:products'))
        self.assertFalse(Product.objects.exists())


class BasketAddViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        gender = Gender.objects.create(name='TestGender')
        self.product = Product.objects.create(name='TestProduct', price=10, quantity=5, gender=gender)
        self.url = reverse('products:basket_add', args=[self.product.id])
        self.data = {
            'quantity': 2
        }

    def test_basket_add_view(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/products/')
        self.assertEqual(Basket.objects.count(), 1)
        basket = Basket.objects.first()
        self.assertEqual(basket.user, self.user)
        self.assertEqual(basket.product, self.product)
        self.assertEqual(basket.quantity, 2)


class BasketRemoveViewTest(TestCase):
    def setUp(self):
        gender = Gender.objects.create(name='TestGender')
        category = ProductCategory.objects.create(name="TestCategory")
        self.product = Product.objects.create(
            name='TestProduct',
            price=10,
            quantity=5,
            gender=gender,
            image=IMAGE_FILE,
        )
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.basket = Basket.objects.create(user=self.user, product=self.product, quantity=1)
        self.url = reverse("products:basket_remove", kwargs={'basket_id': self.basket.id})

    def test_basket_remove_view(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(self.url)

        self.assertRedirects(response, PRODUCT_LIST)
        self.assertFalse(Basket.objects.filter(id=self.basket.id).exists())

    def test_basket_remove_view_unauthenticated(self):
        response = self.client.post(self.url)

        expected_redirect_url = reverse("users:login")
        expected_redirect_url += '?next=' + reverse(
            "products:basket_remove",
            kwargs={'basket_id': self.basket.id}
        )
        self.assertRedirects(response, expected_redirect_url)
