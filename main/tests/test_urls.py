from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from http import HTTPStatus

from django.urls import reverse

from main.models import Hat, Brand
from main.services.main_category import MainCategoryService
from main.services.subcategory import SubcategoryService
from main.utils.product import get_product_sub_model_content_types

User = get_user_model()


class IndexURLTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="username1",
            email="test@gmail.com",
        )

    def setUp(self) -> None:
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.not_authorized_client = Client()

    def test_index_url(self):
        expected_status_code = HTTPStatus.OK.value
        index_path = reverse("main:index")

        for client in self.not_authorized_client, self.authorized_client:
            with self.subTest(client=client):
                response = self.client.get(index_path)
                self.assertEqual(response.status_code, expected_status_code)


class CategoryURLTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="test user", email="emailtest@test.com"
        )
        cls.main_category = MainCategoryService.create(title="main category test")
        cls.subcategory = SubcategoryService.create(
            title="subcategory title",
            main_category=cls.main_category,
            product_content_type=get_product_sub_model_content_types()["Hat"],
        )

    def setUp(self) -> None:
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
                self.assertEqual(response.status_code, expected_status)

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
                self.assertEqual(response.status_code, expected_status)
