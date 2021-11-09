from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        unique=True,
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        null=True,
    )

    USERNAME_FIELD = "email"
    email = models.EmailField(_("email address"), blank=True, unique=True)
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
