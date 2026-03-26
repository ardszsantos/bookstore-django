from django.urls import path
from rest_framework.routers import SimpleRouter

from api.viewsets import BookViewSet, OrderViewSet, StoreInfoView

router = SimpleRouter()
router.register("book", BookViewSet, basename="book")
router.register("order", OrderViewSet, basename="order")

urlpatterns = [
    path("store-info/", StoreInfoView.as_view(), name="store-info"),
] + router.urls
