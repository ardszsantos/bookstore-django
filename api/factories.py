import factory
from django.contrib.auth.models import User

from api.models import Book


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.Faker("password")


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker("sentence", nb_words=3)
    author = factory.Faker("name")
    description = factory.Faker("text", max_nb_chars=200)
    price = factory.Faker("random_int", min=10, max=200)
    published_year = factory.Faker("random_int", min=1900, max=2026)
