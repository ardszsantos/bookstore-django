from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token

from api.models import Book


class Command(BaseCommand):
    help = "Popula o banco com livros e cria usuario com token"

    def handle(self, *args, **options):
        books = [
            {
                "title": "Dom Casmurro",
                "author": "Machado de Assis",
                "price": 35,
                "published_year": 1899,
                "description": "Romance que explora ciume e duvida na sociedade carioca do seculo XIX",
            },
            {
                "title": "O Alquimista",
                "author": "Paulo Coelho",
                "price": 42,
                "published_year": 1988,
                "description": "A jornada de Santiago em busca de seu tesouro pessoal",
            },
            {
                "title": "1984",
                "author": "George Orwell",
                "price": 30,
                "published_year": 1949,
                "description": "Distopia sobre vigilancia e controle totalitario",
            },
            {
                "title": "Clean Code",
                "author": "Robert C. Martin",
                "price": 80,
                "published_year": 2008,
                "description": "Guia pratico para escrever codigo limpo e sustentavel",
            },
            {
                "title": "O Senhor dos Aneis",
                "author": "J.R.R. Tolkien",
                "price": 90,
                "published_year": 1954,
                "description": "Epico de fantasia sobre a jornada para destruir o Um Anel",
            },
            {
                "title": "Harry Potter e a Pedra Filosofal",
                "author": "J.K. Rowling",
                "price": 45,
                "published_year": 1997,
                "description": "O inicio da jornada de Harry no mundo da magia",
            },
            {
                "title": "O Pequeno Principe",
                "author": "Antoine de Saint-Exupery",
                "price": 25,
                "published_year": 1943,
                "description": "Fabula sobre amizade, amor e a essencia da vida",
            },
            {
                "title": "Sapiens",
                "author": "Yuval Noah Harari",
                "price": 55,
                "published_year": 2011,
                "description": "Uma breve historia da humanidade",
            },
        ]

        for b in books:
            Book.objects.get_or_create(title=b["title"], defaults=b)

        user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@bookstore.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            user.set_password("admin123")
            user.save()

        token, _ = Token.objects.get_or_create(user=user)

        self.stdout.write(
            self.style.SUCCESS(f"\n  {Book.objects.count()} livros no banco")
        )
        self.stdout.write(self.style.SUCCESS(f"  Usuario: admin / Senha: admin123"))
        self.stdout.write(self.style.SUCCESS(f"  Token: {token.key}\n"))
