from django.views.defaults import page_not_found
from django.views.generic import TemplateView, ListView, DetailView

from .services.main_category import MainCategoryService
from .services.product import ProductService
from .services.subcategory import SubcategoryService
from .utils.view import send_user_context


class IndexView(TemplateView):
    template_name = "main/index.html"

    @send_user_context
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

    @send_user_context
    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(object_list=object_list, **kwargs)


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

    @send_user_context
    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(object_list=object_list, **kwargs)


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

    @send_user_context
    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(object_list=object_list, **kwargs)


class KidsView(ListView):
    template_name = "main/kids.html"
    context_object_name = "products"

    def get_queryset(self):
        return ProductService.get_all_products(for_kids=True)
