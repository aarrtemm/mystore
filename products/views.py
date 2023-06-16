from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import login_required

from products.models import (
    Product,
    ProductCategory,
    Gender,
    Basket
)

from products.forms import ProductForm


def index(request, *args, **kwargs):
    return render(request, 'products/index.html')


class ProductListView(generic.ListView):
    model = Product
    template_name = "products/products.html"
    context_object_name = "products"
    paginate_by = 6

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        gender_id = self.kwargs.get("gender_id")
        queryset = Product.objects.all()

        if category_id:
            queryset = queryset.filter(categories__id=category_id)
        if gender_id:
            queryset = queryset.filter(gender_id=gender_id)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)

        context["categories"] = ProductCategory.objects.all()
        context["genders"] = Gender.objects.all()

        return context


class ProductDetailView(generic.DetailView):
    model = Product


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


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])
