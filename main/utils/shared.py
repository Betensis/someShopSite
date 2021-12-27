from typing import Iterable


def remove_none(iterable: Iterable) -> list:
    return [item for item in iterable if item is not None]
