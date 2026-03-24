import pytest

from api.models import Book


@pytest.mark.django_db
def test_create_book():
    book = Book.objects.create(
        title="Dom Casmurro",
        author="Machado de Assis",
        description="Um classico da literatura brasileira",
        price=35,
        published_year=1899,
    )

    assert book.id is not None
    assert book.title == "Dom Casmurro"
    assert book.author == "Machado de Assis"
    assert book.price == 35
    assert book.published_year == 1899
