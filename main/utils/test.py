import time
from random import choice
from string import ascii_letters
from typing import TypeVar

from django.contrib.auth import get_user_model

from main.models import Brand, MainCategory, Category, Product

T = TypeVar("T")
User = get_user_model()


def get_rand_str(length: int = 10, symbols: str = ascii_letters) -> str:
    pepper = str(time.time())
    rand_str = "".join([choice(symbols) for _ in range(length)])
    return (rand_str + pepper)[:length]


def create_brand() -> Brand:
    return Brand.objects.create(
        title=get_rand_str(),
    )


def create_main_category():
    return MainCategory.objects.create(title=get_rand_str())


def create_subcategory(main_category: MainCategory) -> Category:
    return Category.objects.create(
        title=get_rand_str(),
        main_category=main_category,
    )


def create_products(amount: int = 5, **product_kwargs) -> list[T]:
    return [_create_product(**product_kwargs) for _ in range(amount)]


def _create_product(**product_kwargs):
    product_kwargs = product_kwargs.copy()
    if product_kwargs.get("category") is None:
        main_category = create_main_category()
        product_kwargs["category"] = create_subcategory(main_category)

    product_kwargs.setdefault(
        "title", Product.__name__ + " test object: " + get_rand_str()
    )
    product_kwargs.setdefault("description", get_rand_str(50))
    product_kwargs.setdefault("price", 150)
    product_kwargs.setdefault("brand", create_brand())
    return Product.objects.create(**product_kwargs)


def create_user(**user_kwargs):
    user_kwargs.setdefault("username", get_rand_str())
    user_kwargs.setdefault("email", get_rand_str() + "@mail.com")
    return User.objects.create_user(**user_kwargs)
