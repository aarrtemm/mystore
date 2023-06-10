from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from users.models import User


class SingUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control py-4", "placeholder": "Enter username"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control py-4", "placeholder": "Enter name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control py-4", "placeholder": "Enter surname"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        "class": "form-control py-4", "placeholder": "Enter email address"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control py-4", "placeholder": "Enter password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control py-4", "placeholder": "Confirm your password"}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
        )


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        "class": "form-control py-4", "placeholder": "Username"}))
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={
        "class": "form-control py-4", "placeholder": "Password"}))

    class Meta:
        model = User
        fields = ("username", "password")
