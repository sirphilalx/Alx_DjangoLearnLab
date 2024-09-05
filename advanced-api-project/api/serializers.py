from rest_framework import serializers
from .models import Book, Author
from datetime import datetime





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
    

class AuthorSerializer(serializers.ModelSerializer):
    # The code below indicates that the books field will contain multiple instances of the BookSerializer. This is appropriate because an author can have multiple books associated with them.
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['name']