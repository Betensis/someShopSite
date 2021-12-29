from typing import Optional

from django.http import Http404
from django.views.generic import ListView, DetailView

from core.services import PageView
from main.utils.service.product import is_valid_sex_name
from .models import MainCategory, Subcategory, Product
from .services.product import ProductService


class IndexView(PageView, ListView):
    template_name = "main/product_list.html"
    context_object_name = "products"
    page_title = 'SomeShopSite'

    def get_queryset(self):
        return ProductService().get_products()

    def get_context_data(self, **kwargs):
        return super().get_context_data() | ListView.get_context_data(self, **kwargs)


class MainCategoryView(PageView, ListView):
    template_name = "main/product_list.html"
    context_object_name = "products"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_category: Optional[MainCategory] = None

    def get_title(self):
        main_category = MainCategory.objects.get_or_none(
            slug=self.kwargs["main_category_slug"]
        )
        if main_category is None:
            return 'Категория'

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

        self.main_category = main_category
        return product_service.sex(sex).main_category(self.main_category).get_products()

    def get_context_data(self, **kwargs):
        return super().get_context_data() | ListView.get_context_data(self, **kwargs)


class SubcategoryView(PageView, ListView):
    template_name = "main/product_list.html"
    context_object_name = "products"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subcategory: Optional[Subcategory] = None

    def get_queryset(self):
        sex = self.kwargs["sex"]
        if sex not in Product.SexChoice:
            raise Http404("invalid sex name")

        product_service = ProductService()
        subcategory = Subcategory.objects.get_or_none(
            slug=self.kwargs["subcategory_slug"]
        )
        if subcategory is None:
            raise Http404()

        self.subcategory = subcategory
        return product_service.sex(sex).subcategory(subcategory).get_products()

    def get_title(self):
        if self.subcategory is None:
            return super(SubcategoryView, self).get_title()

        return self.subcategory.title

    def get_context_data(self, **kwargs):
        return super().get_context_data() | ListView.get_context_data(self, **kwargs)


class ProductDetailView(PageView, DetailView):
    template_name = "main/product_detail.html"
    context_object_name = "product"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product: Optional[Product] = None

    def get_queryset(self):
        sex = self.kwargs["sex"]
        if not is_valid_sex_name(sex):
            raise Http404("invalid sex name")

        products = ProductService.get_products_by_subcategory(
            self.kwargs["subcategory_slug"], sex
        )
        if products is None:
            raise Http404()

        return products

    def get_object(self, queryset=None):
        product = super(ProductDetailView, self).get_object(queryset)
        self.product = product

        return product

    def get_title(self):
        if self.product is None:
            return super().get_title()

        return self.product.category.title + ': ' + self.product.title

    def get_context_data(self, **kwargs):
        return super().get_context_data() | DetailView.get_context_data(self, **kwargs)


class KidsView(PageView, ListView):
    template_name = "main/product_list.html"
    context_object_name = "products"
    page_title = 'Детская одежда'

    def get_queryset(self):
        return ProductService().for_kids(True).get_products()

    def get_context_data(self, **kwargs):
        return super().get_context_data() | ListView.get_context_data(self, **kwargs)
