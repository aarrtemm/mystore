import simplejson as json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
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


class OrderListView(ListView):
    template_name = "orders/order_list.html"
    queryset = Order.objects.all()
    ordering = ("-created", )

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        baskets = Basket.objects.filter(user=self.request.user)

        context["total_amount"] = baskets.total_sum()

        return context


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = "orders/order_form.html"

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)

        context["baskets"] = Basket.objects.filter(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        user = self.request.user
        baskets = Basket.objects.filter(user=user)
        if not baskets:
            return redirect("orders:order-canceled")

        order = Order.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            initiator=user
        )

        basket_history = []
        for basket in baskets:
            basket_history.append(json.dumps(basket.get_json(), use_decimal=True))

        order.basket_history = basket_history
        order.save()
        baskets.delete()

        return redirect("orders:order-success")

