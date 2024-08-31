from django.urls import path, include
from .views import BookViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'book', BookViewSet)

urlpatterns = [
    path('api/books', include(router.urls)),
]