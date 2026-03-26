from django.db import models

from api.models.book import Book


class Order(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
