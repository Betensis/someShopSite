from django.urls import path, include

from . import views

app_name = "account"

urlpatterns = [
    path("signup/", views.AccountCreationView.as_view(), name="signup"),
    path("login/", views.AccountLoginView.as_view(), name="login"),
]
