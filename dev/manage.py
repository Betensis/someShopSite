from dev.custom_funcs import custom_functions_by_args

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


def is_custom_args(argv: list[str]) -> bool:
    return argv[1] in custom_functions_by_args.keys()


def start_custom_func(argv: list[str]):
    func = custom_functions_by_args[argv[1]]
    func(*argv[2:])
