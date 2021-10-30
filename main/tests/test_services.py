from django.test import TestCase

from main.models import MainCategory, Subcategory, Outerwear, Brand
from main.services.main_category import MainCategoryService
from main.utils.product import get_product_sub_model_content_types


class MainCategoryServiceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.main_category = MainCategory.objects.create(title="main category!")
        cls.subcategory = Subcategory.objects.create(
            title="subcategory title",
            main_category=cls.main_category,
            product_content_type=get_product_sub_model_content_types()["Outerwear"],
        )
        cls.brand = Brand.objects.create(title="NIKEEEEEEeee")

        cls.outerwears: list[Outerwear] = []
        for index in range(4):
            cls.outerwears.append(
                Outerwear.objects.create(
                    title=f"outerwear {index}",
                    description=f"long desc {index}",
                    price=213 + index * 10,
                    category=cls.subcategory,
                    brand=cls.brand,
                )
            )

    def test_get_products_by_main_category(self):
        products = MainCategoryService.get_products_by_main_category(self.main_category)
        self.assertListEqual([*products], self.outerwears)
