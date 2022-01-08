from typing import Optional

from django.http import Http404
from django.views.generic import ListView, DetailView

from core.services import PageViewMixin
from main.utils.service.product import is_valid_sex_name
from .config.product import ProductServiceListConfig
from .models import MainCategory, Category, Product
from .services.product import ProductService


class IndexView(PageViewMixin, ListView):
    template_name = "main/index.html"
    context_object_name = "products"

    def get_queryset(self):
        return ProductService(ProductServiceListConfig).get_products()

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | self.get_page_context_data()


class SexView(PageViewMixin, ListView):
    template_name = "main/product_list.html"
    context_object_name = "products"

    def get_title(self):
        if is_valid_sex_name(self.kwargs["sex"]):
            return str(self.kwargs["sex"]).capitalize()

        return super().get_title()

    def get_queryset(self):
        sex = self.kwargs["sex"]
        if not is_valid_sex_name(sex):
            raise Http404()

        return ProductService(ProductServiceListConfig).sex(sex).get_products()

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | self.get_page_context_data()


class MainCategoryView(PageViewMixin, ListView):
    template_name = "main/product_list.html"
    context_object_name = "products"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_title(self):
        main_category = MainCategory.objects.get_or_none(
            slug=self.kwargs["main_category_slug"]
        )
        if main_category is None:
            return "Категория"

        return main_category.title

    def get_queryset(self):
        sex = self.kwargs.get("sex")
        if not is_valid_sex_name(sex):
            raise Http404("invalid sex name")

        product_service = ProductService()
        main_category = MainCategory.objects.get_or_none(
            slug=self.kwargs["main_category_slug"]
        )
        if main_category is None:
            raise Http404()

        return (
            product_service.set_config(ProductServiceListConfig)
            .sex(sex)
            .main_category(main_category)
            .get_products()
        )

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | self.get_page_context_data()


class CategoryView(PageViewMixin, ListView):
    template_name = "main/product_list.html"
    context_object_name = "products"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.category: Optional[Category] = None

    def get_queryset(self):
        sex = self.kwargs["sex"]
        if sex not in Product.SexChoice:
            raise Http404("invalid sex name")

        product_service = ProductService()
        category = Category.objects.get_or_none(slug=self.kwargs["category_slug"])
        if category is None:
            raise Http404()

        self.category = category
        return (
            product_service.set_config(ProductServiceListConfig)
            .sex(sex)
            .category(category)
            .get_products()
        )

    def get_title(self):
        if self.category is None:
            return super(CategoryView, self).get_title()

        return self.category.title

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | self.get_page_context_data()


class ProductDetailView(PageViewMixin, DetailView):
    template_name = "main/product_detail.html"
    context_object_name = "product"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product: Optional[Product] = None

    def get_queryset(self):
        return ProductService().get_products()

    def get_object(self, queryset=None):
        product = super(ProductDetailView, self).get_object(queryset)
        self.product = product

        return product

    def get_title(self):
        if self.product is None:
            return super().get_title()

        return self.product.category.title + ": " + self.product.title

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | self.get_page_context_data()
