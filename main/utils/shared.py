from typing import Iterable, Any, Generator


def remove_none(iterable: Iterable) -> Generator[Any, Any, None]:
    return (item for item in iterable if item is not None)
