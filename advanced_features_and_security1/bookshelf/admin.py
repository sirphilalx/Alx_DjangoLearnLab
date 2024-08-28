# myapp/admin.py
from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('title', 'author', 'publication_year')
    
    # Add filters in the sidebar
    list_filter = ('author', 'publication_year')
    
    # Add search functionality
    search_fields = ('title', 'author')
    
    # Customize the form for adding/editing
    fields = ('title', 'author', 'publication_year')
    
   

# Register the Book model with the custom admin options
admin.site.register(Book, BookAdmin)
