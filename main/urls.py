from django.conf.urls.static import static
from django.urls import path

from core import settings
from . import views

app_name = "main"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("sex/<sex:str>", views.SexView.as_view(), name="sex"),
    path(
        "sex/<str:sex>/main-category/<slug:main_category_slug>/",
        views.MainCategoryView.as_view(),
        name="main-category",
    ),
    path(
        "sex/<str:sex>/category/<slug:category_slug>/",
        views.CategoryView.as_view(),
        name="subcategory",
    ),
    path(
        "sex/<str:sex>/subcategory/<slug:subcategory_slug>/product-detail/<int:pk>/",
        views.ProductDetailView.as_view(),
        name="product-detail",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
