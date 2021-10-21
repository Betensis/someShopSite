from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path

from . import views
from core import settings

app_name = "main"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("main-category/<slug:main_category_slug>", views.test),
    # path("category/<slug:category>", ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
