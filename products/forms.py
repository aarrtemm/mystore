from django import forms

from products.models import Product, ProductCategory


class ProductCreateForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=ProductCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Product
        fields = "__all__"
