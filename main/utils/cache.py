from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key


def get_header_cache_key(email: str):
    return make_template_fragment_key("header", [email])


def delete_cached_header(email: str):
    cache.delete(get_header_cache_key(email))
