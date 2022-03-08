from django.contrib.auth import login as auth_login, authenticate, login
from django.contrib.auth.views import LogoutView, SuccessURLAllowedHostsMixin
from django.shortcuts import resolve_url, redirect
from django.utils.http import url_has_allowed_host_and_scheme, is_safe_url
from django.views.generic import FormView
from django.views.generic.base import TemplateView

from account.forms import AccountCreationForm
from core import settings
from core.services import PageViewMixin


class AccountLoginView(PageViewMixin, SuccessURLAllowedHostsMixin, TemplateView):
    template_name = "account/login.html"
    success_url = settings.LOGIN_REDIRECT_URL
    redirect_authenticated_user = True
    redirect_field_name = "next"

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url(settings.LOGIN_REDIRECT_URL)

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name, self.request.GET.get(self.redirect_field_name, "")
        )
        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ""

    def post(self, request, *args, **kwargs):
        user = authenticate(
            email=request.POST.get("email", ""),
            password=request.POST.get("password", ""),
        )
        if user is None:
            return self.render_to_response(
                self.get_context_data(
                    errors=["Введен неверный логин и/или пароль"],
                    email=request.POST.get("email", ""),
                )
            )

        login(request, user)
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        next_url = self.request.GET.get(self.redirect_field_name)
        if next_url and is_safe_url(next_url, allowed_hosts=settings.ALLOWED_HOSTS):
            return (
                super().get_context_data(**kwargs)
                | self.get_page_context_data()
                | {self.redirect_field_name: next_url}
            )

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
    template_name = "account/logout.html"
    page_title = "Logout"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | self.get_page_context_data()
