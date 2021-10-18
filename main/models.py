from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField


User = get_user_model()


class MainCategory(models.Model):
    class Meta:
        verbose_name = _("основная категория")
        verbose_name_plural = _("основные категории")

    title = models.CharField(
        verbose_name=_("название"),
        max_length=150,
        unique=True,
    )
    slug = AutoSlugField(
        populate_from="title",
        unique=True,
        unique_with="title",
        editable=True,
    )

    def __str__(self):
        return self.title


class Subcategory(models.Model):
    class Meta:
        verbose_name = _("подкатегория")
        verbose_name_plural = _("подкатегории")

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
    slug = AutoSlugField(
        populate_from="title",
        unique=True,
        unique_with="title",
        editable=True,
    )

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

    slug = AutoSlugField(
        populate_from="title",
        unique=True,
        unique_with="title",
        editable=True,
    )

    def __str__(self):
        return self.title


class Item(models.Model):
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
    slug = AutoSlugField(
        populate_from="title",
        unique=True,
        unique_with="title",
        editable=True,
    )
    brand = models.ForeignKey(
        Brand,
        models.CASCADE,
        verbose_name=_("бренд"),
    )

    def __str__(self):
        return self.title


class Shoes(Item):
    class Meta:
        verbose_name = _("обувь")
        verbose_name_plural = _("обувь")


class Hat(Item):
    class Meta:
        verbose_name = _("головной убор")
        verbose_name_plural = _("головные уборы")


class OrderItem(models.Model):
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    ordered = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])


class Order(models.Model):
    customer = models.ForeignKey(
        User,
        models.CASCADE,
    )
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField()
