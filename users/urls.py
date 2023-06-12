from django.urls import path

from users.views import registration, UserLoginView, UserLogoutView

app_name = "users"

urlpatterns = [
    path("register/", registration, name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]
