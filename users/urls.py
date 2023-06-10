from django.urls import path, include

from users.views import UserCreateView, UserLoginView

app_name = "users"

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
]
