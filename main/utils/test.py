import time
from random import choice
from string import ascii_letters
from typing import Type, TypeVar

from django.contrib.auth import get_user_model

from main import models
from main.models import Brand, MainCategory, Subcategory, Product
from main.utils.service.content_type import get_content_model_type_by_model

T = TypeVar("T")
User = get_user_model()


def get_rand_str(length: int = 10, symbols: str = ascii_letters) -> str:
    pepper = str(time.time())
    rand_str = "".join([choice(symbols) for i in range(length)])
    return (rand_str + pepper)[:length]


def create_brand() -> Brand:
    return Brand.objects.create(
        title=get_rand_str(),
    )


def create_main_category():
    return MainCategory.objects.create(title=get_rand_str())


def create_subcategory(
    main_category: MainCategory, product_model: Type[Product]
) -> Subcategory:
    product_content_type = get_content_model_type_by_model(product_model)
    return Subcategory.objects.create(
        title=get_rand_str(),
        main_category=main_category,
        product_content_type=product_content_type,
    )


def create_products(
    product_model: Type[T], amount: int = 5, **product_kwargs
) -> list[T]:
    if not issubclass(product_model, Product) and product_model is not Product:
        raise TypeError(
            "product_model must be subclass Product and dont be instance of Product"
        )

    return [_create_product(product_model, **product_kwargs) for _ in range(amount)]


def _create_product(product_model: Type[Product], **product_kwargs):
    product_kwargs = product_kwargs.copy()
    if product_kwargs.get("category") is None:
        main_category = create_main_category()
        product_kwargs["category"] = create_subcategory(main_category, product_model)

    product_kwargs.setdefault(
        "title", product_model.__name__ + " test object: " + get_rand_str()
    )
    product_kwargs.setdefault("description", get_rand_str(50))
    product_kwargs.setdefault("price", 150)
    product_kwargs.setdefault("brand", create_brand())
    return product_model.objects.create(**product_kwargs)


def create_user(**user_kwargs):
    user_kwargs.setdefault("username", get_rand_str())
    user_kwargs.setdefault("email", get_rand_str() + "@mail.com")
    return User.objects.create_user(**user_kwargs)


def create_hats(**kwargs):
    return create_products(models.Hat, **kwargs)


def create_shoes(**kwargs):
    return create_products(models.Shoes, **kwargs)


def create_outerwears(**kwargs):
    return create_products(models.Outerwear, **kwargs)
