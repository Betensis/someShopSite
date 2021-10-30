from string import ascii_letters
from random import choice
from typing import Type, TypeVar

from main.models import Brand, MainCategory, Subcategory, Product
from main.utils.content_type import get_content_model_type_by_model


T = TypeVar("T")


def get_rand_str(length: int = 10, symbols: str = ascii_letters) -> str:
    return "".join([choice(symbols) for i in range(length)])


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
            "product_model должен быть подклассом Product и не быть самим классом Product"
        )

    return [_create_product(product_model, **product_kwargs) for _ in range(amount)]


def _create_product(product_model: Type[Product], **product_kwargs):
    product_kwargs = product_kwargs.copy()
    if product_kwargs.get("category") is None:
        main_category = create_main_category()
        product_kwargs["category"] = create_subcategory(main_category, product_model)

    product_kwargs.setdefault("title", get_rand_str())
    product_kwargs.setdefault("description", get_rand_str(50))
    product_kwargs.setdefault("price", 150)
    product_kwargs.setdefault("brand", create_brand())
    return product_model.objects.create(**product_kwargs)
