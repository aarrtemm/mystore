from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import LoginView

from .forms import SingUpForm, UserLoginForm
from .models import User


class UserCreateView(generic.CreateView):
    model = User
    form_class = SingUpForm
    success_url = reverse_lazy("users:login")


class UserLoginView(LoginView):
    form_class = UserLoginForm
    success_url = reverse_lazy("products:index")
    template_name = "registration/login.html"

