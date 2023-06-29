from django.db import models

from Mystore import settings
from products.models import Basket, Product


class Order(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=255)
    purchased_goods = models.ManyToManyField(Product)
    quantity = models.PositiveSmallIntegerField(default=0)
    address = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    initiator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order #{self.id}. {self.first_name} {self.last_name}"

    def calculate_total_sum(self):
        total_sum = sum([product.total_price() for product in self.purchased_goods.all()])
        return total_sum
