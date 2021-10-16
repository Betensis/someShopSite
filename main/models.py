from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField


class MainCategory(models.Model):
    class Meta:
        verbose_name = _("Основная категория")
        verbose_name_plural = _("Основные категории")

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


class Subcategory(models.Model):
    class Meta:
        verbose_name = _("Подкатегория")
        verbose_name_plural = _("Подкатегории")

    title = models.CharField(
        verbose_name=_("название"),
        max_length=150,
        unique=True,
    )
    main_category = models.ForeignKey(
        MainCategory,
        on_delete=models.CASCADE,
        related_name="subcategories",
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Brand(models.Model):
    class Meta:
        verbose_name = _("бренд")
        verbose_name_plural = _("бренды")

    title = models.CharField(
        verbose_name=_("название"),
        max_length=150,
        unique=True,
    )

    def __str__(self):
        return self.title


class Product(models.Model):
    class Meta:
        abstract = True

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
    )

    def __str__(self):
        return self.title


class Shoes(Product):
    class Meta:
        verbose_name = _("Обувь")
        verbose_name_plural = _("Обувь")


class Hat(Product):
    class Meta:
        verbose_name = _("головной убор")
        verbose_name_plural = _("головные уборы")
