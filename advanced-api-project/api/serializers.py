from rest_framework import serializers
from .models import Book, Author
from datetime import datetime


class Author(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """Check that the publication year is not in the future."""
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value