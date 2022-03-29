from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Model
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField

User = get_user_model()


class BaseManager(models.Manager):
    def get_or_none(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            return None


class BaseModel(models.Model):
    class Meta:
        abstract = True

    objects = BaseManager()


class MainCategory(BaseModel):
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
        db_index=True,
    )

    def __str__(self):
        return self.title


class Category(BaseModel):
    class Meta:
        verbose_name = _("категория")
        verbose_name_plural = _("категории")

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
        db_index=True,
    )

    def __str__(self):
        return self.title


class Brand(BaseModel):
    class Meta:
        verbose_name = _("бренд")
        verbose_name_plural = _("бренды")

    title = models.CharField(
        verbose_name=_("название"),
        max_length=150,
        unique=True,
    )
    description = models.TextField(
        verbose_name=_("описание"),
        max_length=350,
    )
    slug = AutoSlugField(
        populate_from="title",
        unique=True,
        unique_with="title",
        editable=True,
        db_index=True,
    )

    def __str__(self):
        return self.title


class ProductInfoTags(BaseModel):
    class Meta:
        verbose_name = _("Инфо тег")
        verbose_name_plural = _("Инфо теги")

    title = models.CharField(max_length=50, unique=True, verbose_name=_("название"))

    def __str__(self):
        return self.title


class Product(BaseModel):
    class Meta:
        verbose_name = _("Продукт")
        verbose_name_plural = _("Продукты")

    class SexChoice(models.TextChoices):
        MAN = _("man")
        WOMAN = _("woman")

    title = models.CharField(
        verbose_name=_("название"),
        max_length=100,
    )
    care = models.CharField(verbose_name=_("уход"), max_length=150)
    description = models.TextField(
        verbose_name=_("описание"),
    )
    price = MoneyField(
        verbose_name=_("цена"),
        decimal_places=2,
        default_currency="RUB",
        max_digits=14,
        db_index=True,
    )
    category = models.ForeignKey(
        Category,
        models.CASCADE,
        verbose_name=_("категория"),
        db_index=True,
    )
    image = models.ImageField(
        _("фотокарточка"),
        null=True,
    )
    brand = models.ForeignKey(
        Brand,
        models.CASCADE,
        null=True,
        verbose_name=_("бренд"),
        db_index=True,
    )
    sex = models.CharField(
        verbose_name=_("пол"),
        max_length=7,
        choices=SexChoice.choices,
        db_index=True,
        blank=True,
        null=True,
    )
    info_tags = models.ManyToManyField(
        ProductInfoTags,
    )

    def __str__(self):
        return self.title


class ProductWarehouseInfo(BaseModel):
    class Meta:
        verbose_name = _("Складская информация о продуктах")
        verbose_name_plural = _("Складская информация о продуктах")

    class SizeChoice(models.TextChoices):
        XXS = "XXS"
        XS = "XS"
        S = "S"
        M = "M"
        L = "L"
        XL = "XL"
        XXL = "XXL"

    product = models.ForeignKey(
        "Product",
        models.CASCADE,
    )
    product_size = models.CharField(
        choices=SizeChoice.choices,
        verbose_name=_("размер вещи"),
        max_length=8,
        null=True,
    )
    product_quantity = models.PositiveIntegerField(
        verbose_name=_("количество вещей"),
        default=1,
    )

    def __str__(self):
        return str(self.product) + ": " + self.product_size
