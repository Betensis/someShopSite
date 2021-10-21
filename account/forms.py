from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from account.models import Account


class AccountCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ("email",)


class AccountLoginForm(AuthenticationForm):
    class Meta:
        model = Account
        fields = ("email",)
