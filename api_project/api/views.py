
from rest_framework import  viewsets
from .models import Book
from .serializers import BookSerializer
from .views import BookList
# generics.ListAPIView



class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer