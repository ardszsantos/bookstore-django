from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Book


class StoreInfoView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        total_books = Book.objects.count()
        cheapest = Book.objects.order_by("price").values("title", "price").first()
        newest = (
            Book.objects.order_by("-published_year")
            .values("title", "published_year")
            .first()
        )

        return Response(
            {
                "store": "Bookstore Django REST",
                "total_books": total_books,
                "cheapest_book": cheapest,
                "newest_book": newest,
            }
        )
