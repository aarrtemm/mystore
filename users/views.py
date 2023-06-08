from django.urls import reverse_lazy
from django.views import generic

from .forms import SingUpForm
from .models import User


class UserCreateView(generic.CreateView):
    model = User
    form_class = SingUpForm
    success_url = reverse_lazy("products:index")