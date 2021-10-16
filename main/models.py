from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField


class MainCategory(models.Model):
    title = models.CharField(
        verbose_name=_("название"),
        max_length=150,
        unique=True,
    )
    slug = models.SlugField(
        unique=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Основная категория")
        verbose_name_plural = _("Основные категории")


class Subcategory(models.Model):
    title = models.CharField(
        verbose_name=_("название"),
        max_length=150,
        unique=True,
    )
    main_category = models.ForeignKey(
        MainCategory,
        on_delete=models.CASCADE,
        related_name="subcategory",
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _("Подкатегория")
        verbose_name_plural = _("Подкатегории")


class Brand(models.Model):
    title = models.CharField(
        verbose_name=_("название"),
        max_length=150,
        unique=True,
    )


class Product(models.Model):
    title = models.CharField(
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
    )
    image = models.ImageField(
        _("фотокарточка"),
    )
    slug = models.SlugField(
        unique=True,
    )
    brand = models.ForeignKey(
        Brand,
        models.CASCADE,
        verbose_name=_("бренд"),
        related_name="products",
    )

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Shoes(Product):
    class Meta:
        verbose_name = _("Обувь")
        verbose_name_plural = _("Обувь")
