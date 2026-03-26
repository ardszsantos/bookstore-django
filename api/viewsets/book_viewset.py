from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.models import Book
from api.pagination import BookPagination
from api.serializers import BookSerializer


class BookViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def get_queryset(self):
        return Book.objects.all().order_by("id")
