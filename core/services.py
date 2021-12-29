from typing import Optional

from django.contrib.auth import get_user_model
from django.views.generic.base import ContextMixin, View

from core import settings

User = get_user_model()


class PageTitleMixin:
    page_title: Optional[str] = settings.SITE_NAME

    def get_title(self):
        return self.page_title


class PageTitleContextMixin(PageTitleMixin, ContextMixin):
    page_title_context_name = 'title'

    def get_context_data(self, **kwargs):
        context = super(PageTitleContextMixin, self).get_context_data(**kwargs)
        context[self.page_title_context_name] = self.get_title()
        return context


class UserContextView(ContextMixin, View):
    user_context_name: str = "user"

    def get_context_data(self, **kwargs):
        context = super(UserContextView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class PageView(PageTitleContextMixin, UserContextView):
    def get_context_data(self):
        return UserContextView.get_context_data(self) | PageTitleContextMixin.get_context_data(self)
