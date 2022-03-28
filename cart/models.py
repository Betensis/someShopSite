from django.contrib.auth import get_user_model
from django.db import models
from phone_field import PhoneField

from main.models import BaseModel, Product, ProductWarehouseInfo

User = get_user_model()


class Order(BaseModel):
    class Status(models.TextChoices):
        IN_PROCESS = "IN_PROCESS"
        WAITING = "WAITING"
        DONE = "DONE"

    def __str__(self):
        return f"{self.user}: {self.status}"

    user = models.ForeignKey(User, models.DO_NOTHING, related_name="orders")
    contact_email = models.EmailField(null=False)
    contact_phone = PhoneField(null=False)
    contact_place = models.CharField(max_length=150, null=False, blank=False)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.IN_PROCESS
    )
    products_warehouse_info = models.ManyToManyField(
        ProductWarehouseInfo,
        related_name="orders",
    )
