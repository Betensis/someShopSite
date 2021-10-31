from functools import wraps
from typing import Callable


def send_user_context(func: Callable[[...], dict]):
    @wraps(func)
    def wrap(self, *args, **kwargs):
        context = func(self, *args, **kwargs)
        context.setdefault('user', self.request.user)
        return context
    return wrap
