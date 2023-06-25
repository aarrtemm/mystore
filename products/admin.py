from django.contrib import admin

from products.models import ProductCategory, Gender, Product, Basket


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "quantity", "gender")
    search_fields = ("name",)
    list_filter = ("gender", "categories")


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    pass
