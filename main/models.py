from django.db import models
from django.utils.translation import gettext_lazy as _


class MainCategory(models.Model):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=150,
        unique=True,
    )

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=150,
        unique=True,
    )
    main_category = models.ForeignKey(
        MainCategory,
        on_delete=models.CASCADE,
        related_name=_("subcategory"),
    )

    def __str__(self):
        return f"{self.name}"
