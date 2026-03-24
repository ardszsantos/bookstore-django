from rest_framework.routers import SimpleRouter

from api.viewsets import BookViewSet

router = SimpleRouter()
router.register("book", BookViewSet, basename="book")

urlpatterns = router.urls
