from main.models import Product


def is_valid_sex_name(sex) -> bool:
    return type(sex) is str and sex in Product.SexChoice
