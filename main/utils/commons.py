from typing import Iterable, Any


def remove_none(iterable: Iterable) -> list:
    return [item for item in iterable if item is not None]