from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import FormView

from account.forms import AccountCreationForm, AccountLoginForm
from core import settings
from core.services import PageViewMixin


class AccountLoginView(LoginView, PageViewMixin):
    template_name = "account/login.html"
    form_class = AccountLoginForm
    success_url = settings.LOGIN_REDIRECT_URL
    redirect_authenticated_user = False

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | self.get_page_context_data()


class AccountCreationView(FormView, PageViewMixin):
    template_name = "account/signup.html"
    form_class = AccountCreationForm
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | self.get_page_context_data()


class AccountLogoutView(LogoutView, PageViewMixin):
    next_page = settings.LOGOUT_REDIRECT_URL
    template_name = "account/logout.html"
    page_title = "Logout"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | self.get_page_context_data()
