from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, LogoutView

from .forms import SingUpForm, UserLoginForm, UserProfileForm
from products.models import Basket



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
    form = UserProfileForm()
    if request.method == "POST":
        form = UserProfileForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("users:profile"))
        else:
            print(form.errors)

    else:
        form = UserProfileForm(instance=request.user)
    context = {
        "form": form,
        "baskets": Basket.objects.filter(user=request.user)
    }
    return render(request, "registration/profile.html", context=context)
