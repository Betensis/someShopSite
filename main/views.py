from django.http import Http404
from django.views.defaults import page_not_found
from django.views.generic import TemplateView, ListView, DetailView

from .models import MainCategory, Subcategory, Product
from .services.product import ProductService
from .utils.product import is_valid_sex_name
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
        sex = self.kwargs.get("sex")
        if not is_valid_sex_name(sex):
            raise Http404("invalid sex name")

        product_service = ProductService()
        main_category = MainCategory.objects.get_or_none(
            slug=self.kwargs["main_category_slug"]
        )
        if main_category is None:
            return []

        return product_service.sex(sex).main_category(main_category).get_products()

    @send_user_context
    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(object_list=object_list, **kwargs)


class SubcategoryView(ListView):
    template_name = "main/subcategory.html"
    context_object_name = "products"

    def get_queryset(self):
        sex = self.kwargs["sex"]
        if sex not in Product.SexChoice:
            raise Http404("invalid sex name")

        product_service = ProductService()
        subcategory = Subcategory.objects.get_or_none(
            slug=self.kwargs["subcategory_slug"]
        )
        if subcategory is None:
            return page_not_found(self.request)

        return product_service.sex(sex).subcategory(subcategory).get_products()

    @send_user_context
    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(object_list=object_list, **kwargs)


class ProductDetailView(DetailView):
    template_name = "main/product_detail.html"
    context_object_name = "product"

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
    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(object_list=object_list, **kwargs)


class KidsView(ListView):
    template_name = "main/kids.html"
    context_object_name = "products"

    def get_queryset(self):
        return ProductService().for_kids(True).get_products()
