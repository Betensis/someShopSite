from collections.abc import Iterable
from typing import Callable, TypeVar

T = TypeVar("T")


def get_value_by_rule(iterable: Iterable[T], rule: Callable[[T], bool]):
    for item in iterable:
        if rule(item):
            return item
    raise ValueError("Item by rule not found")
