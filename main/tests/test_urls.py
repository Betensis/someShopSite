from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from http import HTTPStatus

from django.urls import reverse

from main.services.main_category import MainCategoryService
from main.services.subcategory import SubcategoryService

User = get_user_model()


class IndexTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="username1",
            email="test@gmail.com",
        )

    def setUp(self) -> None:
        self.authenticated_client = Client()
        self.authenticated_client.force_login(self.user)

        self.not_authenticated_client = Client()

    def test_index_url(self):
        expected_status_code = HTTPStatus.OK.value
        index_path = reverse("main:index")

        for client in self.not_authenticated_client, self.authenticated_client:
            with self.subTest(client=client):
                response = self.client.get(index_path)
                self.assertEqual(response.status_code, expected_status_code)


class MainCategoryTest(TestCase):
    def setUpTestData(cls):
        cls.main_category = MainCategoryService.create(title="main category test")
        cls.subcategory = SubcategoryService.create(
            title="subcategory title",
            main_category=cls.main_category,
        )
