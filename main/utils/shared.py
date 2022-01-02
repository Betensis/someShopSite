from typing import Iterable, Any, Generator, TypeVar

T = TypeVar("T")


def remove_none(iterable: Iterable[T]) -> Generator[T, None, None]:
    return (item for item in iterable if item is not None)
