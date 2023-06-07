from django.shortcuts import render
from django.views import generic

from products.models import Product, ProductCategory, Gender


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
