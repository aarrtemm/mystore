from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Gender(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="products_images")
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
