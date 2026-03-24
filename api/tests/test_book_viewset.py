import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from api.factories import BookFactory, UserFactory


@pytest.mark.django_db
class TestBookViewSet:
    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.token = Token.objects.create(user=self.user)
        self.book = BookFactory()
        self.url = reverse("book-list", kwargs={"version": "v1"})

    def test_list_books(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_book(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        data = {
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "price": 80,
            "published_year": 2008,
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_list_books_unauthorized(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
