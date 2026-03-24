import pytest

from api.models import Book
from api.serializers import BookSerializer


@pytest.mark.django_db
def test_book_serializer_deserialize():
    data = {
        "title": "O Alquimista",
        "author": "Paulo Coelho",
        "description": "Uma historia sobre seguir seus sonhos",
        "price": 42,
        "published_year": 1988,
    }

    serializer = BookSerializer(data=data)
    assert serializer.is_valid(), serializer.errors

    book = serializer.save()
    assert book.id is not None
    assert book.title == "O Alquimista"
    assert book.author == "Paulo Coelho"


@pytest.mark.django_db
def test_book_serializer_serialize():
    book = Book.objects.create(
        title="1984",
        author="George Orwell",
        price=30,
        published_year=1949,
    )

    serializer = BookSerializer(book)
    data = serializer.data

    assert data["title"] == "1984"
    assert data["author"] == "George Orwell"
    assert data["price"] == 30
    assert data["id"] == book.id
