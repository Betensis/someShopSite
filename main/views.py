from django.shortcuts import get_object_or_404
from django.views.defaults import page_not_found
from django.views.generic import TemplateView, ListView

from .models import MainCategory, Subcategory
from .services.main_category import MainCategoryService


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
        return MainCategoryService.get_items_by_main_category(main_category)


class SubcategoryView(ListView):
    template_name = 'main/subcategory.html'
    context_object_name = 'items'

    def get_queryset(self):
        subcategory = get_object_or_404(Subcategory, slug=self.kwargs['subcategory_slug'])
        ItemClass = subcategory.item_model.model_class()
        if not ItemClass:
            return page_not_found(self.request)
        return ItemClass.objects.filter(category=subcategory)
