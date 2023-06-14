from django.urls import path

from products.views import (
    index,
    ProductListView,
    ProductDetailView,
    basket_add
)

app_name = "products"

urlpatterns = [
    path("", index, name="index"),
    path("products/", ProductListView.as_view(), name="products"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/add/<int:product_id>/", basket_add, name="basket_add"),
]
