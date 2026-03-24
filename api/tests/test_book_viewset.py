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
        self.list_url = reverse("book-list", kwargs={"version": "v1"})
        self.detail_url = reverse(
            "book-detail", kwargs={"version": "v1", "pk": self.book.pk}
        )

    def _auth(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    # LIST
    def test_list_books(self):
        self._auth()
        response = self.client.get(self.list_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

    # CREATE
    def test_create_book(self):
        self._auth()
        data = {
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "price": 80,
            "published_year": 2008,
        }
        response = self.client.post(self.list_url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "Clean Code"

    # RETRIEVE
    def test_retrieve_book(self):
        self._auth()
        response = self.client.get(self.detail_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == self.book.pk

    # UPDATE (PUT)
    def test_update_book(self):
        self._auth()
        data = {
            "title": "Titulo Atualizado",
            "author": "Autor Atualizado",
            "price": 99,
            "published_year": 2020,
        }
        response = self.client.put(self.detail_url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Titulo Atualizado"
        assert response.data["price"] == 99

    # PARTIAL UPDATE (PATCH)
    def test_partial_update_book(self):
        self._auth()
        response = self.client.patch(self.detail_url, {"price": 15})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["price"] == 15

    # DELETE
    def test_delete_book(self):
        self._auth()
        response = self.client.delete(self.detail_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    # AUTH
    def test_list_unauthorized(self):
        response = self.client.get(self.list_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_unauthorized(self):
        data = {"title": "Test", "author": "Test"}
        response = self.client.post(self.list_url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
