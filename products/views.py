from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import View

from products.models import (
    Product,
    ProductCategory,
    Gender,
    Basket
)

from products.forms import ProductForm, GetQuantityProductForm


def index(request, *args, **kwargs):
    return render(request, 'products/index.html')


class ProductListView(generic.ListView):
    model = Product
    template_name = "products/products.html"
    context_object_name = "products"
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()

        category_id = self.request.GET.get("category_id")
        gender_id = self.request.GET.get("gender_id")

        if category_id:
            queryset = queryset.filter(categories__id=category_id)
        if gender_id:
            queryset = queryset.filter(gender__id=gender_id)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)

        context["categories"] = ProductCategory.objects.all()
        context["genders"] = Gender.objects.all()

        return context


class ProductDetailView(generic.DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)

        context["form"] = GetQuantityProductForm()
        context["quantity"] = 1
        return context


class ProductCreateView(generic.CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("products:products")


class ProductUpdateView(generic.UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("products:products")


class ProductDeleteView(generic.DeleteView):
    model = Product
    success_url = reverse_lazy("products:products")


class BasketAddView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        product = get_object_or_404(Product, pk=product_id)
        baskets = Basket.objects.filter(user=request.user, product=product)
        quantity = int(request.POST.get("quantity", 1))

        if quantity > product.quantity:
            return HttpResponse("Unavailable item quantity!")

        if not baskets.exists():
            Basket.objects.create(user=self.request.user, quantity=quantity, product=product)
        else:
            basket = Basket.objects.first()
            basket.quantity += quantity
            basket.save()

        return HttpResponseRedirect(reverse_lazy("products:products"))


class BasketRemoveView(LoginRequiredMixin, View):
    def get(self, request, pk):
        basket = get_object_or_404(Basket, id=pk)
        basket.delete()
        return HttpResponseRedirect(reverse_lazy("users:profile"))
