from django.urls import path
from rest_framework.routers import SimpleRouter

from api.viewsets import BookViewSet, StoreInfoView

router = SimpleRouter()
router.register("book", BookViewSet, basename="book")

urlpatterns = [
    path("store-info/", StoreInfoView.as_view(), name="store-info"),
] + router.urls
