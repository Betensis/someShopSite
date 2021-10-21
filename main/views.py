from django.shortcuts import render
from django.views.generic import TemplateView

from .models import MainCategory
from .services import get_items_by_main_category


class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Titanic"
        return context


def test(request, main_category_slug):
    main_category = MainCategory.objects.get(slug=main_category_slug)
    items = get_items_by_main_category(main_category)
    return render(
        request, "main/main_category.html", context={'items': items}
    )
