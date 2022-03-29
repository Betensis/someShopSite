import os

true_values = (
    "True",
    "true",
    "on",
)
false_values = (
    "False",
    "false",
    "off",
)


def is_variable_exist(var: str) -> bool:
    return var in os.environ.keys()


def get_bool(var: str, default: bool = None) -> bool:
    if not is_variable_exist(var):
        if default is not None or var not in true_values or var not in false_values:
            return default
        raise EnvironmentError(f"Environment variable {var} didn't exist")

    var = os.environ.get(var)
    return var in true_values


def get_str(var: str, default: str = None) -> str:
    if not is_variable_exist(var):
        if default is not None:
            return default
        raise EnvironmentError(f"Environment variable {var} didn't exist")

    return os.environ.get(var)


def get_int(var: str, default: int = None):
    if not is_variable_exist(var):
        if default is not None:
            return default
        raise EnvironmentError(f"Environment variable {var} didn't exist")
    if not var.isnumeric():
        raise EnvironmentError(f"Environment variable {var} isn't numeric")

    return int(os.environ.get(var))
