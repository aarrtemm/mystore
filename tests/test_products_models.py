from django.test import TestCase
from users.models import User
from products.models import Product, ProductCategory, Gender, Basket


class ProductCategoryModelTests(TestCase):
    def test_category_name(self):
        category = ProductCategory.objects.create(name="Category 1")
        self.assertEqual(str(category), "Category 1")


class GenderModelTests(TestCase):
    def test_gender_name(self):
        gender = Gender.objects.create(name="Male")
        self.assertEqual(str(gender), "Male")


class ProductModelTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Product 1",
            price=10,
            quantity=2,
            gender=Gender.objects.create(name="testgender")
        )

    def test_product_name(self):
        self.assertEqual(str(self.product), "Name: Product 1")

    def test_product_sum(self):
        self.assertEqual(self.product.total_price(), 20)


class BasketModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(
            name="Product 1",
            price=10,
            quantity=1,
            gender=Gender.objects.create(name="TestGender")
        )

    def test_basket_str(self):
        basket = Basket.objects.create(user=self.user, product=self.product)
        self.assertEqual(str(basket), "Basket for: testuser | Product: Product 1")

    def test_basket_sum(self):
        basket = Basket.objects.create(user=self.user, product=self.product, quantity=2)
        self.assertEqual(basket.sum_for_basket(), 20)


class BasketQuerySetTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(
            name="Product 1",
            price=10,
            quantity=1,
            gender=Gender.objects.create(name="testname")
        )
        self.basket1 = Basket.objects.create(user=self.user, product=self.product, quantity=2)
        self.basket2 = Basket.objects.create(user=self.user, product=self.product, quantity=3)

    def test_total_quantity(self):
        queryset = Basket.objects.all()
        self.assertEqual(queryset.total_quantity(), 5)

    def test_total_sum(self):
        queryset = Basket.objects.all()
        self.assertEqual(queryset.total_sum(), 50.0)
