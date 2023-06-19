from django.urls import path

from orders.views import OrderCreateView, SuccessTemplateView, CancelTemplateView


app_name = "orders"

urlpatterns = [
    path("create/", OrderCreateView.as_view(), name="create-order"),
    path("order-success/", SuccessTemplateView.as_view(), name="order-success"),
    path("order-canceled/", CancelTemplateView.as_view(), name="order-canceled"),
]