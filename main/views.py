from django.views.defaults import page_not_found
from django.views.generic import TemplateView, ListView, DetailView

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
    context_object_name = "products"

    def get_queryset(self):
        main_category = MainCategoryService.get_object_or_404(
            slug=self.kwargs["main_category_slug"],
        )
        return MainCategoryService.get_products_by_main_category(main_category)


class SubcategoryView(ListView):
    template_name = "main/subcategory.html"
    context_object_name = "products"

    def get_queryset(self):
        subcategory = SubcategoryService.get_object_or_404(
            slug=self.kwargs["subcategory_slug"]
        )
        products = SubcategoryService.get_products_by_subcategory(subcategory)
        if products is None:
            return page_not_found(self.request)
        return products


class ProductDetailView(DetailView):
    template_name = "main/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        subcategory = SubcategoryService.get_object_or_404(
            slug=self.kwargs["subcategory_slug"]
        )
        products = SubcategoryService.get_products_by_subcategory(subcategory)
        if products is None:
            return page_not_found(self.request)
        return products
