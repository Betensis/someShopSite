from abc import ABC, abstractmethod


class Config(ABC):
    @classmethod
    @abstractmethod
    def get_config(cls):
        pass
