import inspect
from typing import Type

from django.contrib.contenttypes.models import ContentType

from main import models
from main.models import Product
from main.utils.service.content_type import get_content_model_type_by_model


def get_product_sub_models() -> dict[str, Type[models.Product]]:
    """
    :return: Возвращает словарь, где сопостовляется имя наследников Product и их класс
    """
    # Выбираем все подклассы Product
    product_models = filter(
        lambda x: inspect.isclass(x[1]) and issubclass(x[1], models.Product),
        models.__dict__.items(),
    )
    # Удаляем из product_models класс Product
    product_sub_class_models = filter(
        lambda x: x[1] is not models.Product, product_models
    )
    return dict(product_sub_class_models)


def get_product_sub_model_content_types() -> dict[str, Type[ContentType]]:
    """
    Возвращает словарь где каждому названию класса наследника Product сопоставляется его значение
    :return:
    """
    product_sub_class_models = get_product_sub_models()
    product_content_types = map(
        lambda x: (x[0], get_content_model_type_by_model(x[1])),
        product_sub_class_models.items(),
    )
    return dict(product_content_types)


def is_valid_sex_name(sex) -> bool:
    return type(sex) is str and sex in Product.SexChoice
