from django.test import TestCase

from main.models import Outerwear, Hat, Subcategory
from main.services.main_category import MainCategoryService
from main.services.subcategory import SubcategoryService
from main.utils import test as test_utils


class MainCategoryServiceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.outerwears: list[Outerwear] = test_utils.create_products(
            Outerwear,
            amount=10,
        )

    def test_get_products_by_main_category(self):
        main_category = self.outerwears[0].category.main_category
        products = MainCategoryService.get_products_by_main_category(main_category)
        self.assertListEqual([*products], self.outerwears)


class SubcategoryServiceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.main_category = test_utils.create_main_category()
        cls.subcategory_with_hats = test_utils.create_subcategory(
            cls.main_category, Hat
        )
        cls.hats = test_utils.create_products(
            Hat,
            amount=15,
            category=cls.subcategory_with_hats,
        )
        # Добавил таким образом, т.к. должен сохраняться порядок создания подкатегорий
        cls.subcategories = [cls.subcategory_with_hats] + [
            test_utils.create_subcategory(cls.main_category, Hat) for _ in range(3)
        ]

    def test_get_subcategories_by_main_category(self):
        subcategories = SubcategoryService.get_subcategories_by_main_category(
            self.main_category
        )
        self.assertListEqual([*subcategories], self.subcategories)

    def test_get_products_by_subcategory(self):
        products = SubcategoryService.get_products_by_subcategory(
            self.subcategory_with_hats
        )
        self.assertListEqual([*products], self.hats)
