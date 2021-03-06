from django.contrib.auth.forms import UserCreationForm

from account.models import Account


class AccountCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ("email",)
