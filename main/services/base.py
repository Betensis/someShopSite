from django.db import models
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404


class BaseService:
    pass


class BaseModelService(BaseService):
    model: models.Model

    def __init__(self, model):
        self.model = model

    @classmethod
    def all(cls) -> QuerySet:
        return cls.model.objects.all()

    @classmethod
    def filter(cls, *args, **kwargs) -> QuerySet:
        return cls.model.objects.filter(*args, **kwargs)

    @classmethod
    def get(cls, *args, **kwargs) -> QuerySet:
        return cls.model.objects.get(*args, **kwargs)

    @classmethod
    def get_or_create(cls, defaults=None, **kwargs) -> QuerySet:
        return cls.model.objects.get_or_create(defaults, **kwargs)

    @classmethod
    def get_object_or_404(cls, *args, **kwargs):
        return get_object_or_404(cls.model, *args, **kwargs)
