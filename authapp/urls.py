from django.urls import path
from .views import UserLoginView, UserCreateView
from django.contrib.auth.views import LogoutView

app_name = "authapp"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="/auth/login/"), name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
]
