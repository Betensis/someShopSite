from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField


class MainCategory(models.Model):
    name = models.CharField(
        verbose_name=_("название"),
        max_length=150,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Основная категория")
        verbose_name_plural = _("Основные категории")


class Subcategory(models.Model):
    name = models.CharField(
        verbose_name=_("название"),
        max_length=150,
        unique=True,
    )
    main_category = models.ForeignKey(
        MainCategory,
        on_delete=models.CASCADE,
        related_name="subcategory",
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("Подкатегория")
        verbose_name_plural = _("Подкатегории")


class Product(models.Model):
    name = models.CharField(
        verbose_name=_("название"),
        max_length=150,
        unique=True,
    )
    description = models.TextField(
        verbose_name=_("описание"),
    )
    price = MoneyField(
        verbose_name=_("цена"),
        decimal_places=2,
        default_currency="RUB",
        max_digits=14,
    )
    category = models.ForeignKey(
        Subcategory,
        models.CASCADE,
        verbose_name=_("категория"),
        related_name="products",
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Shoes(Product):
    class Meta:
        verbose_name = _("Обувь")
        verbose_name_plural = _("Обувь")
