from typing import Optional, Iterable
from typing import overload

from django.contrib.auth import get_user_model

from cart.models import Cart
from main.models import Product

User = get_user_model()


class CartService:
    _model = Cart

    def get_products_count_from_current_cart(self, user: User):
        cart = self._model.objects.get_or_none(user=user, is_bought=False)
        if cart is None:
            return 0
        return cart.products.all().count()

    def get_cart(self, user: User) -> Optional[Cart]:
        """
        :return: current cart (cart with is_bought attr equals False) or None
        """
        return self._model.objects.get_or_none(user=user, is_bought=False)

    def add_product_to_cart(self, cart: Cart):
        pass

    def add_products(self, user: User, products: Iterable[Product], create_cart_if_not_exist: bool = True):
        if not user.is_authenticated:
            raise ValueError('User must be authenticated')

        cart = self.get_cart(user)
        if cart is None:
            if create_cart_if_not_exist:
                pass
        cart.products.add(products)