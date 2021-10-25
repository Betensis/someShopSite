from django.views.generic import TemplateView, ListView

from .services.main_category import MainCategoryService
from .services.subcategory import SubcategoryService


class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Titanic"
        return context


class MainCategoryView(ListView):
    template_name = "main/main_category.html"
    context_object_name = "items"

    def get_queryset(self):
        main_category = MainCategoryService.get_object_or_404(slug=self.kwargs["main_category_slug"],)
        return MainCategoryService.get_products_by_main_category(main_category)


class SubcategoryView(ListView):
    template_name = "main/subcategory.html"
    context_object_name = "items"

    def get_queryset(self):
        subcategory = SubcategoryService.get_object_or_404(slug=self.kwargs['subcategory_slug'])
        return SubcategoryService.get_products_by_subcategory(subcategory)
