from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from http import HTTPStatus

from django.urls import reverse

from main.models import Hat, Subcategory, Product, Outerwear, Shoes
from main.services.main_category import MainCategoryService
from main.services.subcategory import SubcategoryService
from main.utils.product import (
    get_product_sub_model_content_types,
    get_product_sub_models,
)
from main.utils import test as test_utils

User = get_user_model()

error_expected_status_msg = "Неверный статус ответа на пути {}"


class IndexURLTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = test_utils.create_user()

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.not_authorized_client = Client()

    def test_index_url(self):
        expected_status_code = HTTPStatus.OK.value
        index_path = reverse("main:index")

        for client in self.not_authorized_client, self.authorized_client:
            with self.subTest(client=client):
                response = self.client.get(index_path)
                self.assertEqual(
                    response.status_code,
                    expected_status_code,
                    error_expected_status_msg.format(index_path),
                )


class CategoryURLTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = test_utils.create_user()
        cls.main_category = test_utils.create_main_category()
        cls.subcategory = test_utils.create_subcategory(
            cls.main_category,
            Hat
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.not_authorized_client = Client()

    def test_main_category_url(self):
        main_category_path = reverse(
            "main:main-category",
            kwargs={
                "main_category_slug": self.main_category.slug,
            },
        )
        expected_status = HTTPStatus.OK.value

        for client in self.not_authorized_client, self.authorized_client:
            with self.subTest():
                response = client.get(main_category_path)
                self.assertEqual(
                    response.status_code,
                    expected_status,
                    error_expected_status_msg.format(main_category_path),
                )

    def test_subcategory_url(self):
        subcategory_path = reverse(
            "main:subcategory",
            kwargs={
                "subcategory_slug": self.subcategory.slug,
            },
        )
        expected_status = HTTPStatus.OK.value

        for client in self.not_authorized_client, self.authorized_client:
            with self.subTest():
                response = client.get(subcategory_path)
                self.assertEqual(
                    response.status_code,
                    expected_status,
                    error_expected_status_msg.format(subcategory_path),
                )


class ProductDetailURLTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = test_utils.create_user()
        cls.main_category = test_utils.create_main_category()
        cls.brand = test_utils.create_brand()

        product_models = (Hat, Outerwear, Shoes)

        def create_subcategory_by_model(model_name: str) -> tuple[Subcategory, Product]:
            subcategory = SubcategoryService.create(
                title=f"subcategory {model_name} title",
                main_category=cls.main_category,
                product_content_type=get_product_sub_model_content_types()[model_name],
            )
            obj = get_product_sub_models()[model_name].objects.create(
                title=f"{model_name}: {cls.brand} title",
                price=123,
                category=subcategory,
                description=f"very very very long {model_name} desc",
                brand=cls.brand,
            )
            return subcategory, obj

        cls.subcategories = [
            test_utils.create_subcategory(cls.main_category, product_model)
            for product_model in product_models
        ]

        cls.products = [
            test_utils.create_products(
                product_model,
                amount=1,
                category=cls.subcategories[index]
            )[0]
            for index, product_model in enumerate(product_models)
        ]

        cls.product_by_subcategory = dict(
            zip(cls.subcategories, cls.products)
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.not_authorized_client = Client()

    def test_product_detail_url(self):
        expected_status = HTTPStatus.OK.value

        for client in self.not_authorized_client, self.authorized_client:
            for subcategory, product in self.product_by_subcategory.items():
                with self.subTest(subcategory=subcategory, product=product):
                    product_detail_path = reverse(
                        "main:product-detail",
                        kwargs={
                            "subcategory_slug": subcategory.slug,
                            "pk": product.pk,
                        },
                    )
                    response = client.get(product_detail_path)
                    self.assertEqual(
                        response.status_code,
                        expected_status,
                        error_expected_status_msg.format(product_detail_path),
                    )


class KidsURLTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = test_utils.create_user()

    def setUp(self) -> None:
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.not_authorized_client = Client()

    def test_kids_url(self):
        expected_status = HTTPStatus.OK.value
        kids_path = reverse(
                        'main:kids'
                    )

        for client in self.authorized_client, self.not_authorized_client:
            with self.subTest():
                response = client.get(
                    kids_path
                )
                self.assertEqual(response.status_code, expected_status)
