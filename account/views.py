from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView
from django.views.generic import FormView

from account.forms import AccountCreationForm, AccountLoginForm
from core import settings


class AccountLoginView(LoginView):
    template_name = "account/login.html"
    form_class = AccountLoginForm
    success_url = settings.LOGIN_REDIRECT_URL
    redirect_authenticated_user = False


class AccountCreationView(FormView):
    template_name = "account/signup.html"
    form_class = AccountCreationForm
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return super().form_valid(form)
