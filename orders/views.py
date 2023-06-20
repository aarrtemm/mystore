from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    TemplateView,
    ListView,
    DetailView,
)

from orders.models import Order
from orders.forms import OrderForm
from products.models import Basket


class SuccessTemplateView(TemplateView):
    template_name = "orders/success.html"


class CancelTemplateView(TemplateView):
    template_name = "orders/canceled.html"


class OrderListView(LoginRequiredMixin, ListView):
    template_name = "orders/order_list.html"
    model = Order
    ordering = ("-created", )

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = "orders/order_form.html"
    success_url = reverse_lazy("orders:order-success")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["baskets"] = Basket.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form):
        user = self.request.user
        baskets = Basket.objects.filter(user=user)
        if not baskets.exists():
            return redirect("orders:order-canceled")

        order = form.save(commit=False)
        order.initiator = user
        order.save()

        basket_history = {}
        for basket in baskets:
            basket_history[str(basket.id)] = basket.get_json()

        order.basket_history = basket_history
        order.save()

        for basket in baskets:
            order.purchased_goods.add(basket.product)
        baskets.delete()

        return super().form_valid(form)
