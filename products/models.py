from django.db import models

from users.models import User


class ProductCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Gender(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to="products_images",
        null=True,
        blank=True,
        default="media/images/example.jpg"
    )
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    categories = models.ManyToManyField(ProductCategory)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)

    def __str__(self):
        return f"Name: {self.name}"

    def sum(self):
        return self.price * self.quantity


class BasketQuerySet(models.QuerySet):

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def total_sum(self):
        return sum(basket.sum() for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f"Basket for: {self.user.username} | Product: {self.product.name}"

    def sum(self):
        return self.product.price * self.quantity

    def get_json(self):
        basket_item = {
            "product_name": self.product.name,
            "quantity": self.quantity,
            "price": float(self.product.price),
            "sum": float(self.sum())
        }
        return basket_item
