from django.conf.global_settings import ALLOWED_HOSTS
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from account.consts import NEXT_URL_QUERY_PARAM_NAME


def redirect_with_next(next_url: str, *args, **kwargs):
    if not url_has_allowed_host_and_scheme(next_url, ALLOWED_HOSTS):
        raise ValueError(f"Unsafe next url: {next_url}")

    login_path = reverse("account:login")
    result_path = f"{login_path}?{NEXT_URL_QUERY_PARAM_NAME}={next_url}"

    return redirect(result_path, *args, **kwargs)
