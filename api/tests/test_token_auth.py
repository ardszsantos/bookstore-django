import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from api.factories import BookFactory, UserFactory


@pytest.mark.django_db
class TestTokenAuthentication:
    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.book_url = reverse("book-list", kwargs={"version": "v1"})

    def test_create_token_for_user(self):
        token = Token.objects.create(user=self.user)
        assert token.key is not None
        assert len(token.key) == 40
        assert token.user == self.user

    def test_one_token_per_user(self):
        Token.objects.create(user=self.user)
        with pytest.raises(Exception):
            Token.objects.create(user=self.user)

    def test_access_with_valid_token(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        response = self.client.get(self.book_url)
        assert response.status_code == status.HTTP_200_OK

    def test_access_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token abc123fakeinvalid")
        response = self.client.get(self.book_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_access_without_token(self):
        response = self.client.get(self.book_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_book_with_token(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        data = {"title": "Test Book", "author": "Test Author", "price": 50}
        response = self.client.post(self.book_url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_book_without_token(self):
        data = {"title": "Test Book", "author": "Test Author", "price": 50}
        response = self.client.post(self.book_url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestStoreInfoPublic:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse("store-info", kwargs={"version": "v1"})

    def test_access_without_auth(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_response_data(self):
        BookFactory(title="Livro Barato", price=10, published_year=2020)
        BookFactory(title="Livro Novo", price=50, published_year=2025)

        response = self.client.get(self.url)
        assert response.data["store"] == "Bookstore Django REST"
        assert response.data["total_books"] == 2
        assert response.data["cheapest_book"]["title"] == "Livro Barato"
        assert response.data["newest_book"]["title"] == "Livro Novo"

    def test_empty_store(self):
        response = self.client.get(self.url)
        assert response.data["total_books"] == 0
        assert response.data["cheapest_book"] is None
        assert response.data["newest_book"] is None
