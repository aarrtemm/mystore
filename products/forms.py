from django import forms

from products.models import Product, ProductCategory


class ProductForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=ProductCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Product
        fields = "__all__"
