from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from main.models import BaseModel, Product

User = get_user_model()


class Cart(BaseModel):
    user = models.ForeignKey(
        User,
        models.CASCADE
    )
    is_bought = models.BooleanField(
        verbose_name=_('Уже куплено'),
        default=False,
    )
    products = models.ManyToManyField(
        Product,
        related_name='carts',
    )
