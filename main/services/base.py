from django.db import models
from django.db.models import QuerySet


class BaseService:
    model: models.Model = None

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
