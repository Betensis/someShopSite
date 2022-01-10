from abc import abstractmethod
from enum import Enum, auto
from typing import Iterable

from main.config.base import Config


class ProductServiceConfig(Config):
    class Settings(Enum):
        SELECT_RELATED_FIELDS = auto()
        PREFETCH_RELATED_FIELDS = auto()
        SELECTED_VALUES = auto()

    @classmethod
    @abstractmethod
    def get_config(cls) -> dict[Settings, Iterable]:
        pass


class ProductServiceListConfig(ProductServiceConfig):
    @classmethod
    def get_config(cls):
        return {
            cls.Settings.SELECT_RELATED_FIELDS: ["brand"],
            cls.Settings.PREFETCH_RELATED_FIELDS: [],
            cls.Settings.SELECTED_VALUES: ['pk', "title", "brand__title", "image"],
        }
