from django.urls import path

from api import views

app_name = "api"

urlpatterns = [
    path("add-product-to-cart/", views.test, name="add-product-to-cart"),
]
