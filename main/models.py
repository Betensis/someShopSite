from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Model
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField

from core import settings

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

    slug = AutoSlugField(
        populate_from="title",
        unique=True,
        unique_with="title",
        editable=True,
        db_index=True,
    )

    def __str__(self):
        return self.title


class ProductInfoTags(models.Model):
    class Meta:
        verbose_name = _("Инфо тег")
        verbose_name_plural = _("Инфо теги")

    title = models.CharField(max_length=50, unique=True, verbose_name=_("название"))

    def __str__(self):
        return self.title


class Product(BaseModel):
    class SexChoice(models.TextChoices):
        MAN = _("man")
        WOMAN = _("woman")

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
        verbose_name=_("бренд"),
        db_index=True,
    )
    sex = models.CharField(
        verbose_name=_("пол"),
        max_length=7,
        choices=SexChoice.choices,
        db_index=True,
        blank=True,
    )

    info_tags = models.ManyToManyField(
        ProductInfoTags,
    )

    def __str__(self):
        return self.title


# class OrderProduct(models.Model):
#     customer = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#     )
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey("content_type", "object_id")
#     quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
#     order = models.ForeignKey(
#         "Order",
#         on_delete=models.CASCADE,
#         related_name="products",
#     )
#
#     def get_content_type_repr(self):
#         return str(self.content_type).split("|")[1]
#
#     def __str__(self):
#         return f"{self.customer} {self.get_content_type_repr()} id:{self.object_id}"
#
#
# class Order(models.Model):
#     customer = models.ForeignKey(
#         User,
#         models.CASCADE,
#     )
#     ordered_date = models.DateTimeField()
#     ordered = models.BooleanField()
#
#     def __str__(self):
#         return f"{self.customer.email}: " + ", ".join(
#             map(
#                 lambda item: item.get_content_type_repr() + f" id:{item.object_id}",
#                 self.products.all()[:3],
#             )
#         )
