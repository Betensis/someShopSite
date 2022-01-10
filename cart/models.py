from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from main.models import BaseModel, Product, ProductWarehouseInfo

User = get_user_model()


class Cart(BaseModel):
    def __str__(self):
        is_bought_represent = "Уже куплено" if self.is_bought else "Еще не куплено"
        return str(self.user) + ": " + is_bought_represent

    user = models.ForeignKey(User, models.CASCADE)
    is_bought = models.BooleanField(
        verbose_name=_("Уже куплено"),
        default=False,
    )
    products_warehouse_info = models.ManyToManyField(
        ProductWarehouseInfo,
        related_name="carts",
    )
