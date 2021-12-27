from django.http import Http404
from django.views.generic import ListView, DetailView

from main.utils.service.product import is_valid_sex_name
from .models import MainCategory, Subcategory, Product
from .services.product import ProductService
from .utils.view import send_user_context


class PageTitleContextMixin:
    page_title = None

    def get_page_title(self):
        if self.page_title is None:
            raise NotImplementedError("Attribute page_title must be set")
        return self.page_title


class IndexView(ListView, PageTitleContextMixin):
    template_name = "main/product_list.html"
    context_object_name = "products"
    page_title = "SomeShopSite"

    def get_queryset(self):
        return ProductService().get_products()

    @send_user_context
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["title"] = self.get_page_title()
        return context


class MainCategoryView(ListView, PageTitleContextMixin):
    template_name = "main/product_list.html"
    context_object_name = "products"

    def get_page_title(self):
        main_category = MainCategory.objects.get_or_none(
            slug=self.kwargs["main_category_slug"]
        )
        return main_category.title if main_category is not None else ""

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

        return product_service.sex(sex).main_category(main_category).get_products()

    @send_user_context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_page_title()
        return context


class SubcategoryView(ListView, PageTitleContextMixin):
    template_name = "main/product_list.html"
    context_object_name = "products"

    def get_page_title(self):
        subcategory = Subcategory.objects.get(slug=self.kwargs["subcategory_slug"])
        return subcategory.title

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

        return product_service.sex(sex).subcategory(subcategory).get_products()

    @send_user_context
    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(object_list=object_list, **kwargs)


class ProductDetailView(DetailView, PageTitleContextMixin):
    template_name = "main/product_detail.html"
    context_object_name = "product"
    page_title = ""

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

    @send_user_context
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class KidsView(ListView, PageTitleContextMixin):
    template_name = "main/product_list.html"
    context_object_name = "products"
    page_title = "Детская Одежда"

    def get_queryset(self):
        return ProductService().for_kids(True).get_products()

    @send_user_context
    def get_context_data(self, **kwargs):
        context = super(KidsView, self).get_context_data(**kwargs)
        context["title"] = self.get_page_title()

        return context
