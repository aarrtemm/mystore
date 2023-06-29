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


class GetQuantityProductForm(forms.ModelForm):
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={
        "type": "number",
        "class": "form-control text-center w-100",
        "name": "quantity",
        "id": "quantity",
    }))

    class Meta:
        model = Product
        fields = ("quantity", )
