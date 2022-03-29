from typing import Optional

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView

from cart.exceptions import CartDoesNotExist
from cart.services import CartService
from cart.services.order import OrderService
from core.services import PageViewMixin
from main.exception import ProductNotAvailableException
from main.services import ProductWarehouseInfoService


@method_decorator(login_required, "dispatch")
class CartView(PageViewMixin, ListView):
    template_name = "cart/cart.html"
    context_object_name = "product_infos"
    page_title = "Корзина"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.products_sum: Optional[dict] = None
        self.cart_service = CartService()

    def get_queryset(self):
        cart, _ = self.cart_service.get_or_create_cart(self.request)
        product_infos = self.cart_service.get_all_product_infos_by_cart(cart)
        self.products_sum = self.cart_service.get_products_price_sum(cart)

        return product_infos

    def get_context_data(self, **kwargs):
        return (
            super().get_context_data(**kwargs)
            | self.get_page_context_data()
            | {"products_sum": self.products_sum}
        )


@method_decorator(login_required, "dispatch")
@method_decorator(transaction.atomic, "post")
class OrderView(PageViewMixin, TemplateView):
    template_name = "cart/buy.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.order_service = OrderService()
        self.cart_service = CartService()
        self.product_warehouse_service = ProductWarehouseInfoService()

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | self.get_page_context_data()

    def post(self, request):
        email = request.POST.get("email") or ""
        phone = request.POST.get("phone") or ""
        place = request.POST.get("place") or ""
        if "" in [email, phone, place]:
            return redirect("cart:cart")
        try:
            order = self.order_service.create_order_by_cart(
                request, self.cart_service.get_cart(request), email, phone, place
            )
        except CartDoesNotExist:
            return redirect("main:index")
        except ProductNotAvailableException:
            return redirect("cart:cart")

        return self.render_to_response(
            self.get_context_data() | {"order": order},
        )
