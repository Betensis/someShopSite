from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path("signup/", views.AccountCreationView.as_view(), name="signup"),
    path("login/", views.AccountLoginView.as_view(), name="login"),
    path("logout/", views.AccountLogoutView.as_view(), name="logout"),
]
