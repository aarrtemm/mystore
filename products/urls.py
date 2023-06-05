from django.urls import path

from products.views import index, ProductListView

app_name = "products"

urlpatterns = [
    path("", index, name="index"),
    path("products/", ProductListView.as_view(), name="products")
]