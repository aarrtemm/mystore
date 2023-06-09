from django.urls import path

from products.views import (
    index,
    ProductListView,
    ProductDetailView,
    BasketAddView,
    BasketRemoveView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
)

app_name = "products"

urlpatterns = [
    path("", index, name="index"),
    path("products/", ProductListView.as_view(), name="products"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/add/<int:pk>/", BasketAddView.as_view(), name="basket_add"),
    path("products/remove/<int:pk>/", BasketRemoveView.as_view(), name="basket_remove"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
]
