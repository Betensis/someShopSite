from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView

from .models import MainCategory
from .services import get_items_by_main_category


class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Titanic"
        return context


class MainCategoryView(ListView):
    template_name = 'main/main_category.html'
    context_object_name = 'items'

    def get_queryset(self):
        main_category = get_object_or_404(MainCategory, slug=self.kwargs['main_category_slug'])
        return get_items_by_main_category(main_category)
