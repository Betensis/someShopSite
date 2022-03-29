from typing import Type

from django.contrib.contenttypes.models import ContentType
from django.db.models import Model


def get_content_model_type_by_model(model: Type[Model]):
    return ContentType.objects.get_for_model(model=model)
