from rest_framework.viewsets import ModelViewSet

from api.models import Order
from api.pagination import OrderPagination
from api.serializers import OrderSerializer


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    pagination_class = OrderPagination

    def get_queryset(self):
        return Order.objects.all().order_by("id")
