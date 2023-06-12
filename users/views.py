from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, LogoutView

from .forms import SingUpForm, UserLoginForm
from .models import User


def registration(request):
    form = SingUpForm()
    if request.method == "POST":
        form = SingUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("users:login"))
    else:
        form = SingUpForm()
    context = {"form": form}
    return render(request, "registration/registration.html", context=context)


class UserLoginView(LoginView):
    form_class = UserLoginForm
    success_url = reverse_lazy("products:index")
    template_name = "registration/login.html"


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("users:login")


def profile(request):
    pass
