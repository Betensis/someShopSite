from typing import Type

from main import models
import inspect


def get_product_sub_models() -> dict[str, Type[models.Product]]:
    """
    Возвращает словарь, где сопостовляется имя наследников Product и их класс
    """
    # Выбираем все подклассы Product
    product_models = filter(
        lambda x: inspect.isclass(x[1]) and issubclass(x[1], models.Product),
        models.__dict__.items(),
    )
    # Удаляем из product_models класс Product
    product_models_subclasses = filter(
        lambda x: x[1] is not models.Product, product_models
    )
    return dict(product_models_subclasses)
