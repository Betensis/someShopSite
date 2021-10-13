from pathlib import Path

from core.settings import BASE_DIR

apps = [
    "main",
]

apps_path: list[Path] = [*map(lambda x: BASE_DIR.joinpath(x), apps)]
assert all(map(lambda x: x.exists(), apps_path)), "not all app exist"
