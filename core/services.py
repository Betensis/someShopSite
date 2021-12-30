from typing import Optional

from django.contrib.auth import get_user_model
from django.views.generic.base import ContextMixin, View

from core import settings

User = get_user_model()


class PageTitleMixin:
    page_title: Optional[str] = settings.SITE_NAME

    def get_title(self):
        return self.page_title


class PageTitleContextMixin(PageTitleMixin):
    page_title_context_name = "title"

    def get_page_title_context_data(self):
        return {
            self.page_title_context_name: self.get_title(),
        }


class UserContextView(View):
    user_context_name: str = "user"

    def get_user_context_data(self):
        return {self.user_context_name: self.request.user}


class PageViewMixin(PageTitleContextMixin, UserContextView):
    def get_page_context_data(self):
        return self.get_user_context_data() | self.get_page_title_context_data()
