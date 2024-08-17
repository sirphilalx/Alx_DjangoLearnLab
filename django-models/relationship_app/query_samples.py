# relationship_app/query_samples.py

import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project_name.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def query_books_by_author(author_name):
    """Query all books by a specific author."""
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        print(f"Books by {author_name}:")
        for book in books:
            print(f"- {book.title}")
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")

def list_books_in_library(library_name):
    """List all books in a library."""
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in {library_name}:")
        for book in books:
            print(f"- {book.title} by {book.author.name}")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")

def retrieve_librarian_for_library(library_name):
    """Retrieve the librarian(s) for a library."""
    try:
        library = Library.objects.get(name=library_name)
        librarians = library.librarians.all()
        print(f"Librarians for {library_name}:")
        for librarian in librarians:
            print(f"- {librarian.name}")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")

if __name__ == "__main__":
    # Example usage
    print("Query 1: Books by a specific author")
    query_books_by_author("J.K. Rowling")
    
    print("\nQuery 2: Books in a specific library")
    list_books_in_library("New York Public Library")
    
    print("\nQuery 3: Librarians for a specific library")
    retrieve_librarian_for_library("New York Public Library")