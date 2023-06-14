from django.urls import path

from products.views import (
    index,
    ProductListView,
    ProductDetailView,
    basket_add,
    basket_remove
)

app_name = "products"

urlpatterns = [
    path("", index, name="index"),
    path("products/", ProductListView.as_view(), name="products"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/add/<int:product_id>/", basket_add, name="basket_add"),
    path("products/remove/<int:basket_id>", basket_remove, name="basket_remove")
]
