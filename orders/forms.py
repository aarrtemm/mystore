from django import forms

from orders.models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "John",
        # "required": True
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Smith",
        # "required": True
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "john@example.com"
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Ukraine, Kyiv, St. Petra Sahaidachnoho, 35",
        # "required": True

    }))

    class Meta:
        model = Order
        fields = (
            "first_name",
            "last_name",
            "email",
            "address"
        )
