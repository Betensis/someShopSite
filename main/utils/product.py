from typing import Type
import inspect

from django.contrib.contenttypes.models import ContentType

from main import models
from main.utils.content_type import get_content_model_type_by_model


def get_product_sub_models() -> dict[str, Type[models.Product]]:
    """
    Возвращает словарь, где сопостовляется имя наследников Product и их класс
    :return:
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
