import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from api.factories import BookFactory, UserFactory


@pytest.mark.django_db
class TestBookPagination:
    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        self.url = reverse("book-list", kwargs={"version": "v1"})

    def test_default_page_size(self):
        for _ in range(7):
            BookFactory()

        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 7
        assert len(response.data["results"]) == 5
        assert response.data["next"] is not None

    def test_second_page(self):
        for _ in range(7):
            BookFactory()

        response = self.client.get(self.url, {"page": 2})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2
        assert response.data["previous"] is not None

    def test_custom_page_size(self):
        for _ in range(10):
            BookFactory()

        response = self.client.get(self.url, {"page_size": 3})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 3

    def test_max_page_size_limit(self):
        for _ in range(10):
            BookFactory()

        response = self.client.get(self.url, {"page_size": 100})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 10
