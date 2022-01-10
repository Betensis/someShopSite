from typing import Optional

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView

from cart.services import CartService
from core.services import PageViewMixin


@method_decorator(login_required, "dispatch")
class CartView(PageViewMixin, ListView):
    template_name = "cart/cart.html"
    context_object_name = "product_infos"
    page_title = "Корзина"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.products_sum: Optional[dict] = None

    def get_queryset(self):
        user = self.request.user
        cart_service = CartService()

        cart, _ = cart_service.get_or_create_cart(user)
        product_infos = cart_service.get_all_product_infos_by_cart(cart)
        self.products_sum = cart_service.get_products_sum(cart)

        return product_infos

    def get_context_data(self, **kwargs):
        return (
            super().get_context_data(**kwargs)
            | self.get_page_context_data()
            | {"products_sum": self.products_sum}
        )


class CartBuyView(TemplateView):
    template_name = "cart/buy.html"
