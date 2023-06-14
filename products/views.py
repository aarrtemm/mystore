from django.shortcuts import render, HttpResponseRedirect
from django.views import generic

from products.models import (
    Product,
    ProductCategory,
    Gender,
    Basket
)


def index(request, *args, **kwargs):
    return render(request, 'products/index.html')


class ProductListView(generic.ListView):
    model = Product
    template_name = "products/products.html"
    context_object_name = "products"
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)

        context["categories"] = ProductCategory.objects.all()
        context["genders"] = Gender.objects.all()

        return context


class ProductDetailView(generic.DetailView):
    model = Product


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


def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])