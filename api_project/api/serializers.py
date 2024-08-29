from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.modelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author']