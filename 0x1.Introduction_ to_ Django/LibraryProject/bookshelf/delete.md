# Deleting an insance of the book class

```
from bookshelf.models import Book

# Retrieve the Book instance with the title "Nineteen Eighty-Four"
book = Book.objects.get(title="Nineteen Eighty-Four")

# Delete the Book instance
book.delete()

# Confirm the deletion by trying to retrieve all books
all_books = Book.objects.all()
print(all_books)

```
