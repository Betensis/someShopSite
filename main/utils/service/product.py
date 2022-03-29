from django.db.models import Max

from core import settings
from main.models import Product


def is_valid_sex_name(sex) -> bool:
    return type(sex) is str and sex in Product.SexChoice


def get_image_url_by_name(image_name: str):
    return settings.MEDIA_URL + image_name


def get_max_product_pk() -> int:
    return Product.objects.aggregate(max_pk=Max("pk"))["max_pk"]
